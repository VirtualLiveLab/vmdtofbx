from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from utils.validator import validate

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot
    from app.core.chat.components.view import vote as vote_view

    pass


class Vote(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @app_commands.command(name="vote", description="投票を作成するよ！(最大25択)")
    async def vote(
        self,
        interaction: discord.Interaction,
        question: str,
        option1: str | None = None,
        option2: str | None = None,
        option3: str | None = None,
        option4: str | None = None,
        option5: str | None = None,
        option6: str | None = None,
        option7: str | None = None,
        option8: str | None = None,
        option9: str | None = None,
        option10: str | None = None,
        option11: str | None = None,
        option12: str | None = None,
        option13: str | None = None,
        option14: str | None = None,
        option15: str | None = None,
        option16: str | None = None,
        option17: str | None = None,
        option18: str | None = None,
        option19: str | None = None,
        option20: str | None = None,
        option21: str | None = None,
        option22: str | None = None,
        option23: str | None = None,
        option24: str | None = None,
        option25: str | None = None,
    ):
        await interaction.response.defer(ephemeral=False)
        if interaction.channel is None:
            return

        opts = [
            option1,
            option2,
            option3,
            option4,
            option5,
            option6,
            option7,
            option8,
            option9,
            option10,
            option11,
            option12,
            option13,
            option14,
            option15,
            option16,
            option17,
            option18,
            option19,
            option20,
            option21,
            option22,
            option23,
            option24,
            option25,
        ]

        channel = validate(interaction.channel, discord.TextChannel)
        y_or_n = True if all([opt is None for opt in opts]) else False

        if y_or_n:
            view = vote_view.YesNoVoteView()
            await channel.send(view=view)

        pass


async def setup(bot: "Bot"):
    await bot.add_cog(Vote(bot))
