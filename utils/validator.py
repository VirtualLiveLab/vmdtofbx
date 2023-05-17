from typing import Any, TypeVar

T = TypeVar("T", bound=Any)


def validate(var: Any, expected_type: type):
    if not isinstance(var, type(expected_type)):
        raise TypeError(f"{var} is not a {expected_type}")

    pass
