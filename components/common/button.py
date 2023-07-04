from typing import Literal, TypedDict

import discord
from discord import Emoji, PartialEmoji, ui
from discord.interactions import Interaction


class _ButtonStyleRequired(TypedDict):
    color: Literal["blurple", "grey", "green", "red"]


class ButtonStyle(_ButtonStyleRequired, total=False):
    disabled: bool
    emoji: str | Emoji | PartialEmoji | None
    row: Literal[0, 1, 2, 3, 4]


class Button(ui.Button):  # type: ignore
    def __init__(self, label: str | None = None, /, *, style: ButtonStyle, custom_id: str | None = None):
        __style = discord.ButtonStyle[style.get("color", "grey")]
        __disabled = style.get("disabled", False)
        __emoji = style.get("emoji", None)
        __row = style.get("row", None)
        super().__init__(
            style=__style,
            disabled=__disabled,
            emoji=__emoji,
            row=__row,
            label=label,
            custom_id=custom_id,
        )

    async def callback(self, interaction: Interaction):
        pass


class LinkButton(ui.Button):  # type: ignore
    def __init__(self, label: str | None = None, /, *, url: str, custom_id: str | None = None):
        super().__init__(
            style=discord.ButtonStyle.link,
            url=url,
            label=label,
            custom_id=custom_id,
        )

    async def callback(self, interaction: Interaction):
        pass
