import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from app.core.chat import embed

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class Chat(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def add_reaction_to_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        if (con := message.content) == "miku":
            await message.channel.send("MIKU!")
        elif con == "ミクさん！":
            await message.channel.send("呼んだ？")
        elif "うおうお" in con:
            await message.add_reaction("\N{FISH}")
        elif "ふろ" in con:
            await message.add_reaction("\N{bathtub}")
        elif "Docker" in con:
            await message.add_reaction("\N{whale}")

        return

    @app_commands.command(name="miku", description="ミクさんが返事をしてくれるよ！")  # type: ignore[arg-type]
    @app_commands.guilds(int(os.environ["GUILD_ID"]))
    async def call_miku(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("MIKU!")

    @app_commands.command(name="helloworld", description="Hello World!")  # type: ignore[arg-type]
    @app_commands.guilds(int(os.environ["GUILD_ID"]))
    async def hello_world(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=False)
        emb = embed.user_embed(interaction.user)
        await interaction.followup.send(embed=emb)


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Chat(bot))
