import asyncio
import os

import discord

# import sentry_sdk
from discord.ext import commands

from app import embed
from const.log import command_log, login_log
from utils.file import convert_to_cog, get_cwd, glob_files
from utils.finder import Finder
from utils.logger import getMyLogger

if not __debug__:
    from dotenv import load_dotenv

    load_dotenv()


class Bot(commands.Bot):
    def __init__(self) -> None:
        # self.init_sentry()
        self.config = {"prefix": "!"}
        self.logger = getMyLogger(__name__, level="DEBUG")

        # failed extension list
        self.failed_exts: list[str] = []
        self.failed_views: list[str] = []

        # set to None if you want to sync as global commands
        self.app_cmd_sync_target = discord.Object(int(os.environ["GUILD_ID"]))

        # set intents
        intents = discord.Intents.all()
        intents.typing = False
        intents.presences = False

        super().__init__(
            command_prefix=self.config.get("prefix", "!"),
            intents=intents,
        )

    async def setup_hook(self) -> None:
        await self.set_pre_invoke_hook()
        await self.load_exts()
        await self.sync_app_commands()
        await self.setup_views()

    async def on_ready(self) -> None:
        self.logger.info(login_log(user=self.user, guild_amount=len(self.guilds)))
        channel = await Finder(self).find_channel(int(os.environ["CHANNEL_ID"]), type=discord.TextChannel)
        emb = embed.ready_embed(
            latency=self.latency,
            failed_exts=self.failed_exts,
            failed_views=self.failed_views,
        )
        await channel.send(embed=emb)
        await self.change_presence(activity=discord.Game(name="プロセカ"))

    async def load_exts(self) -> None:
        # load cogs automatically
        # "cog.py" under the "app" directory will loaded
        cwd = get_cwd()
        cog_dir = cwd / "app"
        abs_cog_path = glob_files(cog_dir, "cog.py")
        cogs = [convert_to_cog(path.relative_to(cwd)) for path in abs_cog_path]

        if cogs is None or cogs == []:
            return

        for cog in cogs:
            try:
                await self.load_extension(cog)
                self.logger.debug(f"Loaded {cog}")
            except Exception as e:
                self.logger.exception(f"Failed to load {cog}", exc_info=e)

    async def sync_app_commands(self) -> None:
        try:
            synced = await self.tree.sync(guild=self.app_cmd_sync_target)
        except Exception as e:
            self.logger.exception("Failed to sync application commands", exc_info=e)
        else:
            self.logger.info(f"{len(synced)} Application commands synced successfully")

    async def setup_views(self) -> None:
        pass

    async def set_pre_invoke_hook(self) -> None:
        @self.before_invoke
        async def write_debug_log(ctx: commands.Context) -> None:
            self.logger.debug(command_log(ctx))

    # def init_sentry(self) -> None:
    #     sentry_sdk.init(
    #         dsn=os.environ["SENTRY_DSN"],
    #         # Set traces_sample_rate to 1.0 to capture 100%
    #         # of transactions for performance monitoring.
    #         # We recommend adjusting this value in production.
    #         traces_sample_rate=1.0,
    #     )

    def runner(self) -> None:
        try:
            asyncio.run(self._runner())
        except Exception as e:
            self.logger.critical(e)
            asyncio.run(self.shutdown(status=1))

    async def _runner(self) -> None:
        async with self:
            await self.start(os.environ["DISCORD_BOT_TOKEN"])

    async def shutdown(self, status: int = 0) -> None:
        import sys

        # from sentry_sdk import Hub
        # # shutdown Sentry
        # client = Hub.current.client
        # if client is not None:
        #     client.close(timeout=2.0)

        await self.close()
        sys.exit(status)
