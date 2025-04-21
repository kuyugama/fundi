from contextlib import ExitStack, AsyncExitStack

from fundi.types import InjectionTrace
from fundi import from_, scan, inject, ainject, injection_trace


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


def test_inject_cached():
    def dep() -> type:
        return type("unique type", (object,), {})

    def application(unique_type: type = from_(dep), unique_type1: type = from_(dep)):
        return unique_type is unique_type1

    with ExitStack() as stack:
        is_the_same_type = inject({}, scan(application), stack)

        assert is_the_same_type is True


def test_inject_uncached():
    def dep() -> type:
        return type("unique type", (object,), {})

    def application(unique_type: type = from_(dep), unique_type1: type = from_(dep, caching=False)):
        return unique_type is unique_type1

    with ExitStack() as stack:
        is_the_same_type = inject({}, scan(application), stack)

        assert is_the_same_type is False


def test_injection_trace():
    def dep():
        raise RuntimeError()

    def application(value=from_(dep)): ...

    with ExitStack() as stack:
        try:
            inject({}, scan(application), stack)
        except RuntimeError as exc:
            trace = injection_trace(exc)

            assert isinstance(trace, InjectionTrace)

            assert trace.info.call is application

            assert trace.origin is not None
            assert trace.origin.info.call is dep


def test_generator_exception_awareness():
    dependency_state = None

    def dep():
        nonlocal dependency_state
        dependency_state = "started"
        try:
            yield 111
            dependency_state = "finished"
        except RuntimeError:
            dependency_state = "failed"

    def func(arg: int, arg1: str, arg2: int = from_(dep)) -> str:
        assert dependency_state == "started"

        assert arg == 1
        assert arg1 == "value"
        assert arg2 == 111

        raise RuntimeError()

    try:
        with ExitStack() as stack:
            assert dependency_state is None
            inject({"arg": 1, "arg1": "value"}, scan(func), stack)
    except RuntimeError:
        assert True
    else:
        assert False  # This should never happen

    assert dependency_state == "failed"
