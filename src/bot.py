import asyncio
import json
import logging
import os
from typing import Any

import discord

# import sentry_sdk
from discord.ext import commands

from const.log import command_log, login_log
from utils.logger import getMyLogger

if not __debug__:
    from dotenv import load_dotenv

    load_dotenv()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        # self.init_sentry()
        self.config = self.load_config()
        self.logger = self.get_logger()

        # set to None if you want to sync as global commands
        self.app_cmd_sync_target = discord.Object(int(os.environ["GUILD_ID"]))

        # set intents
        intents = discord.Intents.all()
        intents.typing = False

        super().__init__(
            command_prefix=self.config.get("prefix", "!"),
            intents=intents,
            **kwargs,
        )

    async def setup_hook(self):
        await self.set_pre_invoke_hook()
        await self.load_exts()
        await self.sync_app_commands()
        await self.setup_views()

    async def on_ready(self):
        self.logger.info(login_log(user=self.user, guild_amount=len(self.guilds)))

    async def load_exts(self):
        ext_paths: list[str] = self.config.get("cogs", None)
        if ext_paths is None:
            return

        for ext in ext_paths:
            try:
                await self.load_extension(ext)
            except Exception as e:
                self.logger.exception(f"Failed to load {ext}", exc_info=e)

    async def sync_app_commands(self):
        try:
            await self.tree.sync(guild=self.app_cmd_sync_target)
        except Exception as e:
            self.logger.exception("Failed to sync application commands", exc_info=e)
        else:
            self.logger.info("Application commands synced successfully")

    async def setup_views(self):
        pass

    async def set_pre_invoke_hook(self):
        @self.before_invoke
        async def write_debug_log(ctx: commands.Context) -> None:  # type: ignore
            self.logger.debug(command_log(ctx))

    def load_config(self) -> dict[str, Any]:
        with open("config.json", "r") as f:
            return json.load(f)

    def get_logger(self) -> logging.Logger:
        logger = getMyLogger(__name__)
        try:
            logger.setLevel(self.config.get("log_level", "INFO"))
        except (TypeError, ValueError):
            logger.setLevel("INFO")
        return logger

    # def init_sentry(self) -> None:
    #     sentry_sdk.init(
    #         dsn=os.environ["SENTRY_DSN"],
    #         # Set traces_sample_rate to 1.0 to capture 100%
    #         # of transactions for performance monitoring.
    #         # We recommend adjusting this value in production.
    #         traces_sample_rate=1.0,
    #     )

    def runner(self):
        try:
            asyncio.run(self._runner())
        except Exception as e:
            self.logger.critical(e)
            asyncio.run(self.shutdown(status=1))

    async def _runner(self):
        async with self:
            await self.start(os.environ["DISCORD_BOT_TOKEN"])

    async def shutdown(self, status: int = 0):
        import sys

        # from sentry_sdk import Hub
        # # shutdown Sentry
        # client = Hub.current.client
        # if client is not None:
        #     client.close(timeout=2.0)

        await self.close()
        sys.exit(status)
