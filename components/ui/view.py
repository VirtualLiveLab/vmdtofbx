import asyncio
from typing import TYPE_CHECKING

import discord
from pydantic import BaseModel, ConfigDict, Field

# from components.ui.state import State

if TYPE_CHECKING:
    from components.ui.send import ViewSender


class ViewObject(BaseModel):
    content: str | None = Field(default=None)
    embeds: list[discord.Embed] | None = Field(default=None)
    files: list[discord.File] | None = Field(default=None)
    view: discord.ui.View | None = Field(default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class View:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._loop = loop or asyncio.get_event_loop()
        # self.__states: dict[str, State] = {}
        self.__sender: ViewSender | None = None
        # self.compose()

    # def compose(self) -> None:
    #     d = self.__dict__
    #     for k, v in d.items():
    #         if isinstance(v, State):
    #             self.__states[k] = v

    def export(self) -> ViewObject:
        return ViewObject()

    def sync(self) -> None:
        if self.__sender:
            self._loop.create_task(self.__sender.sync())
