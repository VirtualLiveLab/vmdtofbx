import pytest

from utils.deprecate import deprecate_on, deprecated


def test_deprecated() -> None:
    @deprecated
    def func1() -> int:
        return 1

    @deprecate_on("2021-01-01")
    def func2() -> int:
        return 2

    @deprecate_on("2022/12/31", format="%Y/%m/%d")
    def func3() -> int:
        return 3

    @deprecate_on("2077-01-01")
    def func4() -> int:
        return 4

    with pytest.warns(DeprecationWarning):
        func1()

    with pytest.warns(DeprecationWarning):
        func2()

    with pytest.warns(DeprecationWarning):
        func3()

    with pytest.warns(FutureWarning):
        func4()
