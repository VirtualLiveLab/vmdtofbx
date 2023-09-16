import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from utils.logger import get_my_logger

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class Pin(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        self.logger = get_my_logger(__name__)
        self.ctx_pin_message = app_commands.ContextMenu(
            name="Pin / Unpin",
            guild_ids=[int(os.environ["GUILD_ID"])],
            callback=self.ctx_pin_message_callback,
        )
        self.bot.tree.add_command(self.ctx_pin_message)

    async def ctx_pin_message_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.defer(ephemeral=True)
        author_name = str(interaction.user)

        if message.pinned:
            res = await self.unpin_message(author_name, message)
        else:
            res = await self.pin_message(author_name, message)

        await interaction.followup.send(res, ephemeral=True)

    async def pin_message(self, author: str, message: discord.Message) -> str:
        try:
            await message.pin(reason=f"by {author}")
        except discord.Forbidden:
            response = "権限がありません。"
            self.logger.exception("Forbidden")
        except discord.NotFound:
            response = "チャンネルやメッセージが見つかりませんでした。"
            self.logger.exception("Channel or message not found")
        except discord.HTTPException:
            response = "ピン留めに失敗しました。"
            self.logger.exception("Failed to pin")
        except Exception:
            response = "不明なエラーが発生しました。"
            self.logger.exception("Unknown error")
        else:
            response = "ピン留めしました。"

        return response

    async def unpin_message(self, author: str, message: discord.Message) -> str:
        try:
            await message.unpin(reason=f"by {author}")
        except discord.Forbidden:
            response = "権限がありません。"
            self.logger.exception("Forbidden")
        except discord.NotFound:
            response = "チャンネルやメッセージが見つかりませんでした。"
            self.logger.exception("Channel or message not found")
        except discord.HTTPException:
            response = "ピン留めに失敗しました。"
            self.logger.exception("Failed to pin")
        except Exception:
            response = "不明なエラーが発生しました。"
            self.logger.exception("Unknown error")
        else:
            response = "ピン留めを解除しました。"

        return response


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Pin(bot))
