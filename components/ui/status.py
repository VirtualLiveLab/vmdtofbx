import datetime
from copy import deepcopy

import discord
from discord import Embed, Webhook
from discord.types.embed import Embed as EmbedData

from const.enums import Status
from utils.logger import getMyLogger

# TODO: add loading emoji in VLL and switch to it
INITIALIZED_EMOJI = "\N{Hourglass with Flowing Sand}"
LOADING_EMOJI = "<a:loading:1126058379756978186>"
SUCCESSFUL_EMOJI = "\N{WHITE HEAVY CHECK MARK}"
FAILED_EMOJI = "\N{CROSS MARK}"
PANIC_EMOJI = "\N{COLLISION SYMBOL}"


class StatusContext:
    """
    A context for displaying the status of something.

    Attributes
    ----
    key: `str`
        The key to identify the context.
    message: `str`
        The message to display. This will be appeared in the embed description.
    status: `Status`
        The status of the context. Defaults to `Status.INITIALIZED`.
    """

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
        """
        Returns the string representation of the context.
        """
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
        """
        Set the context to initialized.

        Args
        ----
        message (`str`):
            The message to display.
        """
        self.message = message
        self.status = Status.INITIALIZED

    def to_in_progress(self, *, message: str) -> None:
        """
        Set the context to in progress.

        Args
        ----
        message (`str`):
            The message to display.
        """
        self.message = message
        self.status = Status.IN_PROGRESS

    def to_success(self, *, message: str) -> None:
        """
        Set the context to success.

        Args
        ----
        message (`str`):
            The message to display.
        """
        self.message = message
        self.status = Status.SUCCESS

    def to_failed(self, *, message: str) -> None:
        """
        Set the context to failed.

        Args
        ----
        message (`str`):
            The message to display.
        """
        self.message = message
        self.status = Status.FAILED


class StatusUI:
    """
    An embed UI for displaying the status of contexts.
    """

    def __init__(
        self,
        *,
        color: int = 0x000000,
        title: str | None = None,
        url: str | None = None,
        timestamp: datetime.datetime | None = None,
    ):
        """
        Initialize a status UI.

        Args
        ----
        color (`int`):
            The colour code of the embed. Defaults to 0x000000.
        title (`str` | `None`):
            The title of the embed. Defaults to None.
        url (`str` | `None`):
            The URL of the embed. This will be set as title url. Defaults to None.
        timestamp (`datetime.datetime` | `None`):
            The timestamp of the embed content. This is an aware datetime.
            If a naive datetime is passed, it is converted to an aware
            datetime with the local timezone. Defaults to None.
        """
        self.__contexts: dict[str, StatusContext] = {}
        self.embed_dict = Embed(
            color=color,
            title=title,
            url=url,
            timestamp=timestamp,
        ).to_dict()
        self.__message: discord.Message
        self.__logger = getMyLogger(__name__)

    @property
    def embed_dict(self) -> EmbedData:
        """
        Returns a deepcopy of `Embed.to_dict()`.

        Returns
        -------
        EmbedData:
            `Embed.to_dict()` of the embed.
        """
        return deepcopy(self.__embed_dict)

    @embed_dict.setter
    def embed_dict(self, value: EmbedData) -> None:
        self.__embed_dict = value

    @property
    def color(self) -> int | None:
        """
        Getter
        ----
        Returns the current color of the embed.

        Returns
        ----
        `int` | `None`:
            The color code of the embed.
        """
        return self.embed_dict.get("color", None)

    @color.setter
    def color(self, value: int) -> None:
        """
        Setter
        ----
        Set the color of the embed.

        Args
        ----
        value (`int`):
            The color code to set.
        """
        current = self.embed_dict
        current["color"] = value
        self.embed_dict = current

    def set_message(self, message: discord.Message) -> None:
        """
        Set message object to the UI.\\
        This is required to update the UI.\\
        If you use `StatusUI.send()`, this is automatically set.

        Args
        ----
        message (`discord.Message`):
            The message object to set.
        """
        self.__message = message

    def add(self, *, key: str, status: Status = Status.INITIALIZED, message: str) -> None:
        """
        Add a new status context to the UI.

        Args
        ----
        key (`str`):
            Key of the context.
        message (`str`):
            Message of the context. this will be displayed in the UI.
        status (`Status`):
            Initial status of context. Defaults to Status.INITIALIZED.

        Raises
        ----
        `KeyError`:
            If the `key` already exists.
        """
        if key in self.__contexts.keys():
            raise KeyError(f"Context {key} already exists")
        self.__contexts[key] = StatusContext(key=key, message=message, initial_status=status)
        return

    def remove(self, *, key: str) -> None:
        """
        Remove a status context from the UI.

        Args
        ----
        key (`str`):
            Key of the context you want to remove.

        Raises
        ----
        `KeyError`:
            If the `key` does not exist.
        """
        if key not in self.__contexts.keys():
            raise KeyError(f"Context {key} does not exist")
        self.__contexts.pop(key)
        return

    def update(self, *, key: str, status: Status | None = None, message: str | None = None) -> None:
        """
        Update a status context in the UI.\\
        You must provide at least one of `status` or `message`.

        Args
        ----
        key (`str`):
            Key of the context you want to update.
        status (`Status` | `None`):
            New status of the context. Defaults to None.
        message (`str` | `None`):
            New message of the context. Defaults to None.

        Raises
        ----
        `ValueError`:
            If both `status` and `message` are None.
        `KeyError`:
            If the `key` does not exist.
        """
        if status is None and message is None:
            raise ValueError("At least one of status or message must be provided")
        if key not in self.__contexts.keys():
            raise KeyError(f"Context {key} does not exist")

        if status is not None:
            self.__contexts[key].status = status
        if message is not None:
            self.__contexts[key].message = message
        return

    @property
    def _embed(self) -> Embed:
        """
        Getter
        ----
        Returns the embed object of the UI.\\
        Using this property is not recommended.\\
        Useful if you want to edit the embed directly like `embed.add_field()`.

        Raises
        ----
        `ValueError`: If the description of embed is too long.

        Returns
        ----
        `discord.Embed`
            The embed object of the UI.
        """
        current = self.embed_dict
        description = "\n".join(ctx.to_string() for ctx in self.__contexts.values())
        if len(description) > 4096:
            raise ValueError("Description is too long")
        current["description"] = description
        return Embed.from_dict(current)

    @_embed.setter
    def _embed(self, value: Embed) -> None:
        """
        Setter
        ----
        Set the embed object of the UI.

        Args
        ----
        value (`discord.Embed`):
            The embed object to set.
        """
        self.embed_dict = value.to_dict()

    async def send(
        self,
        target: discord.abc.Messageable | discord.Interaction | Webhook,
        ephemeral: bool = False,
    ) -> None:
        """
        Send the UI to the target.

        Args
        ----
        target (`discord.abc.Messageable` |`discord.Interaction` | `discord.Webhook`):
            The target to send the UI.
        ephemeral: `bool`
            Indicates if the message should only be visible to the user who started the interaction.
            If a view is sent with an ephemeral message and it has no timeout set then the timeout
            is set to 15 minutes. Defaults to `False`.

        Raises
        ----
        `TimeoutError`:
            If the `interaction.token` is expired.
        """
        if isinstance(target, discord.Interaction):
            if target.is_expired():
                raise TimeoutError("Interaction is expired")
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

    async def sync(self) -> None:
        """
        Sync the UI to current state. Fail if both of `StatusUI.set_message()` and `StatusUI.send()` are not called.
        """
        try:
            await self.__message.edit(embed=self._embed)
        except Exception as e:
            self.__logger.error(f"Failed to edit message: {e}")
