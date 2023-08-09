from typing import Any, TypeVar

T = TypeVar("T", bound=Any)


def validate(var: Any, expected_type: type[T]) -> T:  # noqa: ANN401
    if isinstance(var, expected_type):
        return var
    msg = f"{var} is not a {expected_type}"
    raise TypeError(msg)
