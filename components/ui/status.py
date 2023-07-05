import datetime
from copy import deepcopy
from enum import IntEnum, auto
from typing import Any

import discord
from discord import Embed, Webhook
from discord.types.embed import Embed as EmbedData

from utils.logger import getMyLogger

# TODO: add loading emoji in VLL and switch to it
INITIALIZED_EMOJI = "\N{Hourglass with Flowing Sand}"
LOADING_EMOJI = "<a:loading:1126058379756978186>"
SUCCESSFUL_EMOJI = "\N{WHITE HEAVY CHECK MARK}"
FAILED_EMOJI = "\N{CROSS MARK}"
PANIC_EMOJI = "\N{COLLISION SYMBOL}"


class Status(IntEnum):
    INITIALIZED = auto()
    IN_PROGRESS = auto()
    SUCCESS = auto()
    FAILED = auto()


class StatusContext:
    def __init__(self, *, key: str, message: str, initial_status: Status = Status.INITIALIZED) -> None:
        self.key = key
        self.message = message
        self.status = initial_status

    @property
    def key(self) -> str:
        return self.__name

    @key.setter
    def key(self, value: str) -> None:
        self.__name = value

    @property
    def message(self) -> str:
        return self.__label

    @message.setter
    def message(self, value: str) -> None:
        self.__label = value

    @property
    def status(self) -> Status:
        return self.__status

    @status.setter
    def status(self, value: Status) -> None:
        self.__status = value

    def to_string(self) -> str:
        match self.__status:
            case Status.INITIALIZED:
                return f"{INITIALIZED_EMOJI} {self.__label}"
            case Status.IN_PROGRESS:
                return f"{LOADING_EMOJI} {self.__label}"
            case Status.SUCCESS:
                return f"{SUCCESSFUL_EMOJI} {self.__label}"
            case Status.FAILED:
                return f"{FAILED_EMOJI} {self.__label}"
            case _:
                return f"{PANIC_EMOJI} [PANIC OCCURRED] {self.__label}"

    def to_initialized(self, *, message: str) -> None:
        self.message = message
        self.status = Status.INITIALIZED

    def to_in_progress(self, *, message: str) -> None:
        self.message = message
        self.status = Status.IN_PROGRESS

    def to_success(self, *, message: str) -> None:
        self.message = message
        self.status = Status.SUCCESS

    def to_failed(self, *, message: str) -> None:
        self.message = message
        self.status = Status.FAILED


class StatusUI:
    def __init__(
        self,
        *,
        color: int = 0x000000,
        title: Any | None = None,
        url: Any | None = None,
        timestamp: datetime.datetime | None = None,
    ):
        self.contexts = {}
        self.embed_dict = Embed(
            color=color,
            title=title,
            url=url,
            timestamp=timestamp,
        ).to_dict()
        self.__message: discord.Message
        self.__logger = getMyLogger(__name__)

    @property
    def contexts(self) -> dict[str, StatusContext]:
        return self.__contexts

    @contexts.setter
    def contexts(self, value: dict[str, StatusContext]) -> None:
        self.__contexts = value

    @property
    def embed_dict(self) -> EmbedData:
        return deepcopy(self.__embed_dict)

    @embed_dict.setter
    def embed_dict(self, value: EmbedData) -> None:
        self.__embed_dict = value

    @property
    def color(self) -> int | None:
        return self.embed_dict.get("color", None)

    @color.setter
    def color(self, value: int) -> None:
        current = self.embed_dict
        current["color"] = value
        self.embed_dict = current

    def set_message(self, message: discord.Message) -> None:
        self.__message = message

    def add(self, *, key: str, status: Status = Status.INITIALIZED, message: str) -> None:
        if key in self.__contexts.keys():
            raise ValueError(f"Context {key} already exists")
        self.__contexts[key] = StatusContext(key=key, message=message, initial_status=status)
        return

    def remove(self, *, key: str) -> None:
        if key not in self.__contexts.keys():
            raise ValueError(f"Context {key} does not exist")
        self.__contexts.pop(key)
        return

    def update(self, *, key: str, status: Status | None = None, message: str | None = None) -> None:
        if status is None and message is None:
            raise ValueError("At least one of status or message must be provided")
        if key not in self.__contexts.keys():
            raise ValueError(f"Context {key} does not exist")

        if status is not None:
            self.__contexts[key].status = status
        if message is not None:
            self.__contexts[key].message = message
        return

    # def to_embed(self) -> Embed:
    #     current = self.embed_dict
    #     description = "\n".join(ctx.to_string() for ctx in self.contexts.values())
    #     if len(description) > 4096:
    #         raise ValueError("Description is too long")
    #     current["description"] = description
    #     return Embed.from_dict(current)

    @property
    def _embed(self) -> Embed:
        current = self.embed_dict
        description = "\n".join(ctx.to_string() for ctx in self.contexts.values())
        if len(description) > 4096:
            raise ValueError("Description is too long")
        current["description"] = description
        return Embed.from_dict(current)

    @_embed.setter
    def _embed(self, value: Embed) -> None:
        self.embed_dict = value.to_dict()

    async def send(
        self,
        target: discord.abc.Messageable | discord.Interaction | Webhook,
        ephemeral: bool = False,
    ) -> None:
        if isinstance(target, discord.Interaction):
            if target.is_expired():
                raise ValueError("Interaction is expired")
            if target.response.is_done():
                self.__message = await target.followup.send(embed=self._embed, ephemeral=ephemeral, wait=True)
                return
            await target.response.send_message(embed=self._embed, ephemeral=ephemeral)
            self.__message = await target.original_response()
            return

        if isinstance(target, discord.Webhook):
            self.__message = await target.send(embed=self._embed, wait=True, ephemeral=ephemeral)
        else:
            self.__message = await target.send(embed=self._embed)

    async def edit(self) -> None:
        try:
            await self.__message.edit(embed=self._embed)
        except Exception as e:
            self.__logger.error(f"Failed to edit message: {e}")
