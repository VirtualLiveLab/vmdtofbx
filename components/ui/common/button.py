from typing import Literal, TypedDict

import discord
from discord import Emoji, PartialEmoji, ui
from discord.interactions import Interaction

from components.ui.type import InteractionCallback
from components.ui.utils.call import call_any_function


class _ButtonStyleRequired(TypedDict):
    color: Literal["blurple", "grey", "green", "red"]


class ButtonStyle(_ButtonStyleRequired, total=False):
    disabled: bool
    emoji: str | Emoji | PartialEmoji | None
    row: Literal[0, 1, 2, 3, 4]


class Button(ui.Button):
    def __init__(
        self,
        label: str | None = None,
        /,
        *,
        style: ButtonStyle,
        custom_id: str | None = None,
        on_click: InteractionCallback | None = None,
    ) -> None:
        __style = discord.ButtonStyle[style.get("color", "grey")]
        __disabled = style.get("disabled", False)
        __emoji = style.get("emoji", None)
        __row = style.get("row", None)
        self.__callback_fn = on_click
        super().__init__(
            style=__style,
            disabled=__disabled,
            emoji=__emoji,
            row=__row,
            label=label,
            custom_id=custom_id,
        )

    async def callback(self, interaction: Interaction) -> None:
        if self.__callback_fn:
            await call_any_function(self.__callback_fn, interaction)


class LinkButton(ui.Button):
    def __init__(self, label: str | None = None, /, *, url: str, custom_id: str | None = None) -> None:
        super().__init__(
            style=discord.ButtonStyle.link,
            url=url,
            label=label,
            custom_id=custom_id,
        )

    async def callback(self, interaction: Interaction) -> None:
        pass
