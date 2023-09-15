from discord import Embed

from app.core.vote.type import VoteOption
from const.discord import VOTE_FOOTER_MESSAGE
from const.enums import Color


def vote_embed(question: str, option: list[VoteOption]) -> Embed:
    embed = Embed(
        color=Color.MIKU,
        title=question,
    )
    embed.set_author(name="投票")
    embed.set_footer(text=VOTE_FOOTER_MESSAGE)
    for opt in option:
        embed.add_field(name=opt.emoji, value=opt.label)
    return embed


def vote_result_embed(question: str, option: list[VoteOption]) -> Embed:
    embed = Embed(
        color=Color.MIKU,
        title=f"{question}の投票結果",
    )
    for i, opt in enumerate(option):
        embed.add_field(name=f"{i + 1}位: {opt.label}", value=f"**{opt.current}票**", inline=False)

    return embed
