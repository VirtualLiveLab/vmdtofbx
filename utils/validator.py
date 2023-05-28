from typing import Any, TypeVar

T = TypeVar("T", bound=Any)


def validate(var: Any, expected_type: type[T]) -> T:
    if isinstance(var, expected_type):
        return var
    raise TypeError(f"{var} is not a {expected_type}")
