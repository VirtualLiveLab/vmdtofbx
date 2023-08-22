import asyncio
from collections.abc import Callable
from typing import Any, Generic, TypeVar

from components.ui.view import View
from utils.logger import get_my_logger

T = TypeVar("T", bound=Any)


class State(Generic[T]):
    def __init__(self, initial_value: T, view: View, /, *, loop: asyncio.AbstractEventLoop | None = None) -> None:
        self._initial_value: T = initial_value
        self._current_value: T = self._initial_value

        self._loop = loop or asyncio.get_event_loop()
        self._view = view
        self._logger = get_my_logger(self.__class__.__name__)

    def get_state(self) -> T:
        return self._current_value

    def set_state(self, new_value: T | Callable[[T], T]) -> None:
        _new_value: T = self._current_value

        if isinstance(new_value, Callable):
            try:
                r = new_value(self._current_value)
            except Exception:
                self._logger.exception("Error while executing callable")
            else:
                if not isinstance(r, type(self._current_value)):
                    self._logger.warning("Callable returned value of different type")
                else:
                    _new_value = r
        else:
            _new_value = new_value

        self._current_value = _new_value

        if self._view:
            self._view.sync()
