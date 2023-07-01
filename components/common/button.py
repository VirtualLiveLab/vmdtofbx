from typing import Literal, Optional, TypedDict, Union

import discord
from discord import Emoji, PartialEmoji, ui
from discord.interactions import Interaction


class ButtonStyleRequired(TypedDict):
    color: Literal["blurple", "grey", "green", "red"]


class ButtonStyle(ButtonStyleRequired, total=False):
    disabled: bool
    emoji: str | Emoji | PartialEmoji | None
    label: str | None
    row: Literal[0, 1, 2, 3, 4]


class BaseButton(ui.Button):  # type: ignore
    def __init__(
        self,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        label: Optional[str] = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        url: Optional[str] = None,
        emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
        row: Optional[int] = None,
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
        )
        pass

    async def callback(self, interaction: Interaction):
        pass


class Button(BaseButton):
    def __init__(self, *, style: ButtonStyle, custom_id: str | None = None):
        __style = discord.ButtonStyle[style.get("color", "secondary")]
        __disabled = style.get("disabled", False)
        __emoji = style.get("emoji", None)
        __label = style.get("label", None)
        __row = style.get("row", None)
        super().__init__(
            style=__style,
            label=__label,
            disabled=__disabled,
            emoji=__emoji,
            row=__row,
            custom_id=custom_id,
        )

    async def callback(self, interaction: Interaction):
        pass


class LinkButton(BaseButton):
    def __init__(self, *, url: str, label: str, custom_id: str | None = None):
        super().__init__(
            style=discord.ButtonStyle.link,
            url=url,
            label=label,
            custom_id=custom_id,
        )

    async def callback(self, interaction: Interaction):
        pass
