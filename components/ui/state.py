import asyncio
from collections.abc import Callable
from typing import Any, Generic, NamedTuple, TypeVar

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

    def __call__(self) -> T:
        return self._get_state()

    def _get_state(self) -> T:
        return self._current_value

    def _set_state(self, new_value: T | Callable[[T], T]) -> None:
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

        msg = f"State changed: {self._current_value} -> {_new_value}"
        self._logger.debug(msg)
        self._current_value = _new_value

        if self._view:
            self._view.sync()
        else:
            self._logger.warning("View is not set")


class UseStateTuple(NamedTuple, Generic[T]):
    state: State[T]
    set_state: Callable[[T | Callable[[T], T]], None]


def use_state(
    initial_value: T,
    view: View,
    /,
    *,
    loop: asyncio.AbstractEventLoop | None = None,
) -> UseStateTuple[T]:
    s = State[T](initial_value, view, loop=loop)
    return UseStateTuple(state=s, set_state=s._set_state)  # noqa: SLF001
