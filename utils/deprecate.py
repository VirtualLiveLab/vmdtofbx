import warnings
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from typing import ParamSpec, TypeVar, overload

from utils.time import JST

P = ParamSpec("P")
R = TypeVar("R")


def deprecated(func: Callable[P, R]) -> Callable[P, R]:
    """
    decorator to deprecate function.

    Parameters
    ----------
    func : Callable[P, R]
        function to deprecate.

    Returns
    -------
    Callable[P, R]
        deprecated function.

    Raises
    ------
    DeprecationWarning
        deprecated function.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        msg = "Deprecated"
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)

    return wrapper


@overload
def deprecate_on(date: datetime) -> Callable[[Callable[P, R]], Callable[P, R]]:
    ...


@overload
def deprecate_on(date: str, format: str = "%Y-%m-%d") -> Callable[[Callable[P, R]], Callable[P, R]]:  # noqa: A002
    ...


def deprecate_on(date: str | datetime, format: str = "%Y-%m-%d") -> Callable[[Callable[P, R]], Callable[P, R]]:  # noqa: A002
    """
    decorator to deprecate function on specific date.

    Parameters
    ----------
    date : `str` | `datetime` | `None`
        date to deprecate, by default None.

    Returns
    -------
    `Callable[[Callable[P, R]], Callable[P, R]]`
        decorator to deprecate function.
    """

    def _deprecate(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            dt = datetime.strptime(date, format).astimezone(JST()) if isinstance(date, str) else date
            is_deprecated = datetime.now(JST()) > dt

            if is_deprecated:
                msg = f"Deprecated since {date}. This function will be removed in the future."
                warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return _deprecate
