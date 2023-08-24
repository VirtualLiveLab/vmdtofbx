from typing import Literal, TypedDict

from discord import Emoji, Interaction, PartialEmoji, ui
from discord import SelectOption as _SelectOption
from pydantic import BaseModel, ConfigDict, Field

from components.ui.type import SelectCallback
from components.ui.utils.call import call_any_function


class SelectStyle(TypedDict, total=False):
    disabled: bool
    placeholder: str | None
    row: Literal[0, 1, 2, 3, 4]


class SelectOption(BaseModel):
    label: str = Field(min_length=1, max_length=100)
    value: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=100)
    emoji: str | Emoji | PartialEmoji | None = Field(default=None)
    selected_by_default: bool = Field(default=False)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SelectOptions(BaseModel):
    min_values: int | None = Field(default=1, ge=0, le=25)
    max_values: int | None = Field(default=1, ge=1, le=25)
    options: list[SelectOption] = Field(min_length=1, max_length=25)


class Select(ui.Select):
    def __init__(
        self,
        *,
        options: SelectOptions,
        style: SelectStyle,
        custom_id: str | None = None,
        on_select: SelectCallback | None = None,
    ) -> None:
        __disabled = style.get("disabled", False)
        __placeholder = style.get("placeholder", None)
        __row = style.get("row", None)
        __d = {
            "disabled": __disabled,
            "placeholder": __placeholder,
            "row": __row,
            "min_values": options.min_values,
            "max_values": options.max_values,
            "options": [
                _SelectOption(
                    label=option.label,
                    value=option.value or option.label,
                    description=option.description,
                    emoji=option.emoji,
                    default=option.selected_by_default,
                )
                for option in options.options
            ],
        }
        if custom_id:
            __d["custom_id"] = custom_id
        self.__callback_fn = on_select
        super().__init__(**__d)

    async def callback(self, interaction: Interaction) -> None:
        if self.__callback_fn:
            await call_any_function(self.__callback_fn, interaction, self.values)
