from asyncio import iscoroutinefunction
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


async def call_any_function(fn: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    if iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    return fn(*args, **kwargs)
