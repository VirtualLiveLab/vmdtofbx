import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

if TYPE_CHECKING:
    # import some original class
    pass


class SomeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="test")
    async def test_cmd(self, ctx: commands.Context):  # type: ignore
        await ctx.send("test")

    @app_commands.command(name="test")
    @app_commands.guilds(discord.Object(id=int(os.environ["GUILD_ID"])))
    @app_commands.guild_only()
    async def test_app_cmd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send("test")


async def setup(bot: commands.Bot):
    await bot.add_cog((SomeCog(bot)))
