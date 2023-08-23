from typing import Any

import discord

from components.ui.view import View
from utils.logger import get_my_logger


class ViewSender:
    def __init__(
        self,
        view: View,
    ) -> None:
        self.__view = view
        self.__message: discord.Message
        self.__logger = get_my_logger(__name__)

    def _get_view_dict(self, timeout: float | None = None) -> dict[str, Any]:
        d = self.__view.export().model_dump(exclude_none=True)
        view = discord.ui.View(timeout=timeout)
        children = d.pop("children", None)
        if children:
            for c in children:
                view.add_item(c)
        return {"view": view, **d}

    async def send(
        self,
        target: discord.abc.Messageable | discord.Interaction | discord.Webhook,
        *,
        timeout: float | None = None,
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
        t = target
        view_dict = self._get_view_dict(timeout)
        self.__view._sender = self  # noqa: SLF001
        if isinstance(t, discord.Interaction):
            if t.is_expired():
                msg = "Interaction is expired"
                raise TimeoutError(msg)
            if t.response.is_done():
                self.__message = await t.followup.send(**view_dict, ephemeral=ephemeral, wait=True)

                return
            await t.response.send_message(**view_dict, ephemeral=ephemeral)
            self.__message = await t.original_response()
            return

        if isinstance(t, discord.Webhook):
            self.__message = await t.send(**view_dict, wait=True, ephemeral=ephemeral)
        else:
            self.__message = await t.send(**view_dict)

    async def sync(self) -> None:
        """
        Sync the UI to current state. Fail if both of `StatusUI.set_message()` and `StatusUI.send()` are not called.
        """
        view_dict = self._get_view_dict()
        try:
            await self.__message.edit(**view_dict)
        except Exception as e:
            msg = f"Failed to edit message: {e}"
            self.__logger.exception(msg)
