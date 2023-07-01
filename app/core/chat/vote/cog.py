import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from const.enums import Color
from utils.io import read_json

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class Vote(commands.Cog):
    __renamed_options = {f"option{i}": f"選択肢{i}" for i in range(1, 21)}

    def __init__(self, bot: "Bot"):
        self.bot = bot

    @app_commands.command(name="vote", description="最大20択で投票を作成するよ！選択肢をすべて省略するとはい/いいえの投票になるよ！")
    @app_commands.guilds(int(os.environ["GUILD_ID"]))
    @app_commands.rename(**(__renamed_options | {"question": "質問文"}))
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
    ):
        await interaction.response.defer(ephemeral=False)
        if interaction.channel is None:
            return

        valid_opts = [
            opt
            for opt in [
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
            ]
            if opt is not None and opt != ""
        ]

        emoji_dict = read_json(r"const/vote_emoji.json")
        if valid_opts == []:
            option = [
                {"name": emoji_dict["0"], "value": "はい"},
                {"name": emoji_dict["1"], "value": "いいえ"},
            ]
        else:
            option = [{"name": emoji_dict[str(i)], "value": valid_opts[i]} for i in range(len(valid_opts))]

        embed = discord.Embed(
            color=Color.MIKU,
            title=question,
        )
        embed.set_author(name="投票")
        for opt in option:
            embed.add_field(**opt)

        msg = await interaction.followup.send(embed=embed, wait=True)
        for e in [d["name"] for d in option]:
            await msg.add_reaction(e)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Vote(bot))
