from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from app.utils.callback import command_unavailable_callback

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class Reminder(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @app_commands.command(name="reminder", description="リマインダー機能(準備中)")  # type: ignore[arg-type]
    async def reminder(self, interaction: discord.Interaction) -> None:
        await command_unavailable_callback(interaction, ephemeral=True, status="WIP")


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Reminder(bot))
