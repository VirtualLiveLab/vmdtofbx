import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from dispander import dispand

from app.core.chat import embed
from components.ui.common.button import LinkButton
from const.enums import Color

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

        match message.content:
            case "miku":
                await message.channel.send("MIKU!")
            case "ミクさん！":
                await message.channel.send("呼んだ？")
            case "うおうお":
                await message.add_reaction("\N{FISH}")
            case "ふろ":
                await message.add_reaction("\N{bathtub}")
            case "Docker":
                await message.add_reaction("\N{whale}")
            case _:
                pass

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

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        if message.author.id == self.bot.user.id:  # type: ignore[union-attr]
            return

        try:
            extracted = await dispand(message, with_reference=False, accent_color=Color.MIKU)
        except Exception:
            self.bot.logger.exception("dispand error")
            extracted = []

        if extracted is None or extracted == []:
            return

        for fragment in extracted:
            view = discord.ui.View(timeout=None)
            view.add_item(
                LinkButton("元のメッセージ", url=fragment["jump_url"]),
            )

            try:
                await message.channel.send(
                    embeds=fragment["embeds"][:10],
                    view=view,
                )
            except Exception:
                self.bot.logger.exception("dispand error")
        return


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Chat(bot))
