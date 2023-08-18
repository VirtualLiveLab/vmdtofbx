import pytest

from utils.deprecate import deprecate_on, deprecated


@pytest.mark.parametrize(
    ("reason"),
    [
        (None),
        ("reason"),
    ],
)
def test_deprecated(reason: str | None) -> None:
    match = "This function is deprecated." if reason is None else reason
    with pytest.warns(DeprecationWarning, match=match):
        deprecated(reason=reason)(lambda: 0)()


def test_deprecated_typeerror() -> None:
    with pytest.raises(TypeError) as e:
        # this is same as
        # @deprecated("THIS IS DEPRECATED")
        # def func():
        #     return 0
        deprecated("THIS IS DEPRECATED")(lambda: 0)()  # type: ignore[call-overload]
    assert str(e.value) == "Expected callable, got <class 'str'>"


@pytest.mark.parametrize(
    ("date", "format", "reason"),
    [
        ("2022-01-01", None, None),
        ("2022-01-02", None, "reason"),
        ("2022-01-01", "%Y-%m-%d", None),
        ("2022-01-02", "%Y-%m-%d", "reason"),
        ("2022/01/01", "%Y/%m/%d", None),
        ("2022/01/02", "%Y/%m/%d", "reason"),
    ],
)
def test_deprecate_on(date: str, format: str | None, *, reason: str | None) -> None:  # noqa: A002
    with pytest.warns(DeprecationWarning):
        deprecate_on(date, format, reason=reason)(lambda: 0)()


@pytest.mark.parametrize(
    ("date", "format", "reason"),
    [
        ("2077-01-01", None, None),
        ("2077-01-02", None, "reason"),
        ("2077-01-01", "%Y-%m-%d", None),
        ("2077-01-02", "%Y-%m-%d", "reason"),
        ("2077/01/01", "%Y/%m/%d", None),
        ("2077/01/02", "%Y/%m/%d", "reason"),
    ],
)
def test_deprecate_on_future(date: str, format: str | None, reason: str | None) -> None:  # noqa: A002
    match = f"This function will be deprecated on {date}." if reason is None else reason
    with pytest.warns(
        FutureWarning,
        match=match,
    ):
        deprecate_on(date, format, reason=reason)(lambda: 0)()
