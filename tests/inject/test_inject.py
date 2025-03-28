from contextlib import ExitStack, AsyncExitStack

from fundi import from_, scan, inject, ainject


def test_inject_sync():
    def dep():
        pass

    def func(arg: int, arg1: str, arg2: None = from_(dep)) -> str:
        assert arg == 1
        assert arg1 == "value"
        assert arg2 is None

        return "result"

    with ExitStack() as stack:
        result = inject({"arg": 1, "arg1": "value"}, scan(func), stack)

        assert result == "result"


def test_inject_sync_generator():
    dependency_state = None

    def dep():
        nonlocal dependency_state
        dependency_state = "started"
        yield 111
        dependency_state = "finished"

    def func(arg: int, arg1: str, arg2: int = from_(dep)) -> str:
        assert dependency_state == "started"

        assert arg == 1
        assert arg1 == "value"
        assert arg2 == 111

        return "result"

    with ExitStack() as stack:
        assert dependency_state is None
        result = inject({"arg": 1, "arg1": "value"}, scan(func), stack)

        assert result == "result"

    assert dependency_state == "finished"


async def test_inject_async():
    async def dep():
        pass

    async def func(arg: int, arg1: str, arg2: None = from_(dep)) -> str:
        assert arg == 1
        assert arg1 == "value"
        assert arg2 is None

        return "result"

    async with AsyncExitStack() as stack:
        result = await ainject({"arg": 1, "arg1": "value"}, scan(func), stack)

        assert result == "result"


async def test_inject_async_generator():
    dependency_state = None

    async def dep():
        nonlocal dependency_state
        dependency_state = "started"
        yield 111
        dependency_state = "finished"

    async def func(arg: int, arg1: str, arg2: int = from_(dep)) -> str:
        assert dependency_state == "started"

        assert arg == 1
        assert arg1 == "value"
        assert arg2 == 111

        return "result"

    async with AsyncExitStack() as stack:
        assert dependency_state is None
        result = await ainject({"arg": 1, "arg1": "value"}, scan(func), stack)

        assert result == "result"

    assert dependency_state == "finished"
