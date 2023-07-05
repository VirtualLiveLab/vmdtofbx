import datetime
from copy import deepcopy
from typing import Any

from discord import Colour, Embed
from discord.types.embed import Embed as EmbedData

# TODO: add loading emoji in VLL and switch to it
LOADING_EMOJI = "<a:loading:1126058379756978186>"
SUCCESSFUL_EMOJI = "\N{WHITE HEAVY CHECK MARK}"
FAILED_EMOJI = "\N{CROSS MARK}"


class StatusEmbed:
    def __init__(
        self,
        *,
        default_label: str,
        color: int | Colour | None = None,
        colour: int | Colour | None = None,
        title: Any | None = None,
        url: Any | None = None,
        timestamp: datetime.datetime | None = None,
    ):
        self.embed_dict = Embed(
            description=default_label,
            color=color,
            colour=colour,
            title=title,
            url=url,
            timestamp=timestamp,
        ).to_dict()

    @property
    def embed_dict(self) -> EmbedData:
        return deepcopy(self.__embed_dict)

    @embed_dict.setter
    def embed_dict(self, value: EmbedData) -> None:
        self.__embed_dict = value

    def loading(
        self,
        *,
        label: str | None = None,
        color: int | None = None,
    ) -> Embed:
        current = self.embed_dict
        label = label or current.get("description", "")
        new_desc = f"{LOADING_EMOJI} {label}"
        current["description"] = new_desc
        if color is not None:
            current["color"] = color
        return Embed.from_dict(current)

    def success(
        self,
        *,
        label: str | None = None,
        color: int | None = None,
    ) -> Embed:
        current = self.embed_dict
        label = label or current.get("description", "")
        new_desc = f"{SUCCESSFUL_EMOJI} {label}"
        current["description"] = new_desc
        if color is not None:
            current["color"] = color
        return Embed.from_dict(current)

    def fail(
        self,
        *,
        label: str | None = None,
        color: int | None = None,
    ) -> Embed:
        current = self.embed_dict
        label = label or current.get("description", "")
        new_desc = f"{FAILED_EMOJI} {label}"
        current["description"] = new_desc
        if color is not None:
            current["color"] = color
        return Embed.from_dict(current)
