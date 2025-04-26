from fundi import scan, from_, FromType
from fundi.types import Parameter


def test_scan_no_deps():
    def func(arg: int): ...

    info = scan(func)

    assert info.async_ is False
    assert info.generator is False
    assert info.call is func

    assert info.parameters == [Parameter("arg", int, None)]


def test_scan_deps():
    def dep() -> int: ...

    dep_info = scan(dep)

    def func(arg: int = from_(dep)): ...

    info = scan(func)

    assert info.async_ is False
    assert info.generator is False
    assert info.call is func
    assert info.parameters == [Parameter("arg", int, dep_info)]


def test_scan_generator_no_deps():
    def func(arg: int):
        yield arg

    info = scan(func)

    assert info.async_ is False
    assert info.generator is True
    assert info.call is func

    assert info.parameters == [Parameter("arg", int, None)]


def test_scan_generator_deps():
    def dep() -> int: ...

    dep_info = scan(dep)

    def func(arg: int = from_(dep)):
        yield arg

    info = scan(func)

    assert info.async_ is False
    assert info.generator is True
    assert info.call is func
    assert info.parameters == [Parameter("arg", int, dep_info)]


def test_scan_async_no_deps():
    async def func(arg: int):  # noqa
        pass

    info = scan(func)

    assert info.async_ is True
    assert info.generator is False
    assert info.call is func

    assert info.parameters == [Parameter("arg", int, None)]


def test_scan_async_deps():
    def dep() -> int:
        pass

    dep_info = scan(dep)

    async def func(arg: int = from_(dep)):  # noqa
        pass

    info = scan(func)

    assert info.async_ is True
    assert info.generator is False
    assert info.call is func
    assert info.parameters == [Parameter("arg", int, dep_info)]


def test_scan_async_generator_no_deps():
    async def func(arg: int):
        yield arg

    info = scan(func)

    assert info.async_ is True
    assert info.generator is True
    assert info.call is func

    assert info.parameters == [Parameter("arg", int, None)]


def test_scan_async_generator_deps():
    def dep() -> int: ...

    dep_info = scan(dep)

    async def func(arg: int = from_(dep)):
        yield arg

    info = scan(func)

    assert info.async_ is True
    assert info.generator is True
    assert info.call is func
    assert info.parameters == [Parameter("arg", int, dep_info)]


# noinspection PyPep8Naming
def test_scan_FromType():
    class Session: ...

    def dep(arg: FromType[Session]): ...

    info = scan(dep)

    assert info.async_ is False
    assert info.generator is False
    assert info.call is dep
    assert info.parameters == [Parameter("arg", Session, None, resolve_by_type=True)]
