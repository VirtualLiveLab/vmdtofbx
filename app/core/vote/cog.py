import os
from typing import TYPE_CHECKING, ClassVar

import discord
from discord import app_commands
from discord.ext import commands
from pydantic import BaseModel, Field

from const.discord import VOTE_FOOTER_MESSAGE
from const.enums import Color
from utils.io import read_json

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class VoteOption(BaseModel):
    label: str
    emoji: str
    current: int = Field(default=0, ge=0)


class Vote(commands.Cog):
    __renamed_options: ClassVar[dict[str, str]] = {f"option{i}": f"選択肢{i}" for i in range(1, 21)}

    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        self.vote_count_ctx_menu = app_commands.ContextMenu(
            name="投票を集計",
            callback=self.vote_count_callback,
            guild_ids=[int(os.environ["GUILD_ID"])],
        )
        self.bot.tree.add_command(self.vote_count_ctx_menu)

    @app_commands.command(  # type: ignore[arg-type]
        name="vote",
        description="最大20択で投票を作成するよ！選択肢をすべて省略するとはい/いいえの投票になるよ！",
    )
    @app_commands.guilds(int(os.environ["GUILD_ID"]))
    @app_commands.rename(**(__renamed_options | {"question": "質問文"}))
    async def vote(  # noqa: PLR0913
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
    ) -> None:
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
                VoteOption(emoji=emoji_dict["0"], label="はい"),
                VoteOption(emoji=emoji_dict["1"], label="いいえ"),
            ]
        else:
            option = [VoteOption(emoji=emoji_dict[str(i)], label=valid_opts[i]) for i in range(len(valid_opts))]

        embed = discord.Embed(
            color=Color.MIKU,
            title=question,
        )
        embed.set_author(name="投票")
        embed.set_footer(text=VOTE_FOOTER_MESSAGE)
        for opt in option:
            embed.add_field(name=opt.emoji, value=opt.label)

        msg = await interaction.followup.send(embed=embed, wait=True)
        for e in [d.emoji for d in option]:
            await msg.add_reaction(e)
        return

    async def vote_count_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.defer(ephemeral=False)

        if not self.is_vote_message(message.embeds):
            await interaction.followup.send("投票メッセージではありません。", ephemeral=False)
            return

        vote_title = message.embeds[0].title or "NULL"

        options = self.process_vote_message(message)
        sorted_options = sorted(options, key=lambda x: x.current, reverse=True)

        result_message = "\n".join([f"{opt.label}:{opt.current}票" for opt in sorted_options])

        embed = discord.Embed(
            color=Color.MIKU,
            title=f"{vote_title}の投票結果",
            description=result_message,
        )
        await interaction.followup.send(embed=embed, ephemeral=False)
        return

    def is_vote_message(self, embeds: list[discord.Embed]) -> bool:
        if embeds is None or embeds == []:
            return False

        em = embeds[0]
        if em.footer.text is None or em.footer.text != VOTE_FOOTER_MESSAGE:
            return False

        return True

    def process_vote_message(self, message: discord.Message) -> list[VoteOption]:
        em = message.embeds[0]

        return [
            VoteOption(
                label=f.value,
                emoji=f.name,
                current=self.get_reaction_count(message.reactions, f.name),
            )
            for f in em.fields
            if f.value is not None and f.name is not None
        ]

    def get_reaction_count(self, reactions: list[discord.Reaction], emoji: str) -> int:
        r = [r for r in reactions if r.emoji == emoji]
        return r[0].count - 1 if r != [] else 0


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Vote(bot))
