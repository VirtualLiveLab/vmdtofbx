# TODO(@sushi-chaaaan): try to use `typing.deprecated(PEP702)` when python 3.12 is released.  # noqa: FIX002
# https://github.com/sushi-chaaaan/Mikubot-v2/issues/17
import functools
import warnings
from collections.abc import Callable
from datetime import datetime
from typing import ParamSpec, TypeVar, overload

from utils.time import JST

P = ParamSpec("P")
R = TypeVar("R")


@overload
def deprecated(func: Callable[P, R]) -> Callable[P, R]:
    ...


@overload
def deprecated(
    *,
    reason: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    ...


def deprecated(
    func: Callable[P, R] | None = None,
    *,
    reason: str | None = None,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """
    decorator to deprecate function.

    Parameters
    ----------
    reason : `str | None`, optional
        reason of deprecation.

    Returns
    -------
    `Callable[[Callable[P, R]], Callable[P, R]]`
        deprecated function.

    Raises
    ------
    DeprecationWarning
        deprecated function.
    """

    def wrapper(func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        msg = "This function is deprecated." if reason is None else reason
        warnings.warn(msg, DeprecationWarning, stacklevel=3)
        return func(*args, **kwargs)

    if func is not None:
        if not callable(func):
            msg = f"Expected callable, got {type(func)}"
            raise TypeError(msg)
        return functools.wraps(func)(functools.partial(wrapper, func))

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        return functools.wraps(func)(functools.partial(wrapper, func))

    return decorator


@overload
def deprecate_on(date: datetime, *, reason: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    ...


@overload
def deprecate_on(
    date: str,
    format: str | None = None,  # noqa: A002
    *,
    reason: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    ...


def deprecate_on(
    date: str | datetime,
    format: str | None = None,  # noqa: A002
    *,
    reason: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    decorator to deprecate function on specific date.

    Parameters
    ----------
    date : `str` | `datetime` | `None`
        date to deprecate, by default None.

    format : `str | None`, optional
        format of date. used when date is `str`, by default `"%Y-%m-%d"`.

    reason : `str | None`, optional
        reason of deprecation.

    Returns
    -------
    `Callable[[Callable[P, R]], Callable[P, R]]`
        decorator to deprecate function.
    """

    def _deprecate(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            f = "%Y-%m-%d" if format is None else format
            dt = datetime.strptime(date, f).astimezone(JST()) if isinstance(date, str) else date
            is_deprecated = datetime.now(JST()) > dt

            if is_deprecated:
                msg = f"This function is deprecated since {date}.\nThis function will be removed in the future."
                if reason:
                    msg += f"\n{reason}"
                warnings.warn(msg, DeprecationWarning, stacklevel=3)
            else:
                msg = f"This function will be deprecated on {date}.\nThis function will be removed in the future."
                if reason:
                    msg += f"\n{reason}"
                warnings.warn(msg, FutureWarning, stacklevel=3)
            return func(*args, **kwargs)

        return wrapper

    return _deprecate
