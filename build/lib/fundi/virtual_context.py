"""
Virtual context managers are created to replace contextlib.contextmanager
and contextlib.asynccontextmanager decorators.
They are fully typed and distinguishable by FunDIs `scan(...)` function
"""

import types
import typing
import inspect
import warnings
from dataclasses import replace
from collections.abc import Generator, AsyncGenerator
from contextlib import AbstractAsyncContextManager, AbstractContextManager

from .scan import scan
from .types import CallableInfo
from .exceptions import GeneratorExitedTooEarly

__all__ = ["VirtualContextManager", "AsyncVirtualContextManager", "virtual_context"]

T = typing.TypeVar("T")
P = typing.ParamSpec("P")
F = typing.TypeVar("F", bound=types.FunctionType)


class VirtualContextManager(typing.Generic[T, P], AbstractContextManager[T]):
    """
    Synchronous virtual context manager
    """

    def __init__(self, function: typing.Callable[P, Generator[T, None, None]]):
        info = replace(scan(function), generator=False, context=True, call=self)
        self.__fundi_info__: CallableInfo[typing.Any] = info

        self.__wrapped__: typing.Callable[P, Generator[T, None, None]] = function
        self.generator: Generator[T, None, None] | None = None

    def __call__(self, *args: P.args, **kwargs: P.kwargs):
        self.generator = self.__wrapped__(*args, **kwargs)
        return self

    def __enter__(self) -> T:  # pyright: ignore[reportMissingSuperCall, reportImplicitOverride]
        assert self.generator is not None, "Generator not initialized, call __call__ method first"
        try:
            return self.generator.send(None)
        except StopIteration as exc:
            raise GeneratorExitedTooEarly(self.__wrapped__, self.generator) from exc

    def __exit__(  # pyright: ignore[reportImplicitOverride]
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> bool:
        assert self.generator is not None, "Generator not initialized, call __call__ method first"

        try:
            if exc_type is not None:
                self.generator.throw(exc_type, exc_value, traceback)
            else:
                self.generator.send(None)
        except StopIteration:
            pass
        except Exception as exc:
            if exc is exc_value:
                return False

            raise exc
        else:
            warnings.warn("Generator not exited", UserWarning)
        return False


class AsyncVirtualContextManager(typing.Generic[T, P], AbstractAsyncContextManager[T]):
    """
    Asynchronous virtual context manager
    """

    def __init__(self, function: typing.Callable[P, AsyncGenerator[T]]):
        info = replace(scan(function), generator=False, context=True, call=self)
        self.__fundi_info__: CallableInfo[typing.Any] = info

        self.__wrapped__: typing.Callable[P, AsyncGenerator[T]] = function
        self.generator: AsyncGenerator[T] | None = None

    def __call__(self, *args: P.args, **kwargs: P.kwargs):
        self.generator = self.__wrapped__(*args, **kwargs)
        return self

    async def __aenter__(self) -> T:  # pyright: ignore[reportImplicitOverride]
        assert self.generator is not None, "Generator not initialized, call __call__ method first"
        try:
            return await self.generator.asend(None)
        except StopAsyncIteration as exc:
            raise GeneratorExitedTooEarly(self.__wrapped__, self.generator) from exc

    async def __aexit__(  # pyright: ignore[reportImplicitOverride]
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> bool:
        assert self.generator is not None, "Generator not initialized, call __call__ method first"

        try:
            if exc_type is not None:
                await self.generator.athrow(exc_type, exc_value, traceback)
            else:
                await self.generator.asend(None)
        except StopAsyncIteration:
            pass
        except Exception as exc:
            if exc is exc_value:
                return False

            raise exc
        else:
            warnings.warn("Generator not exited", UserWarning)
        return False


@typing.overload
def virtual_context(
    function: typing.Callable[P, Generator[T, None, None]],
) -> VirtualContextManager[T, P]: ...
@typing.overload
def virtual_context(
    function: typing.Callable[P, AsyncGenerator[T]],
) -> AsyncVirtualContextManager[T, P]: ...
def virtual_context(
    function: typing.Callable[P, Generator[T, None, None] | AsyncGenerator[T]],
) -> VirtualContextManager[T, P] | AsyncVirtualContextManager[T, P]:
    """
    Define virtual context manager using decorator

    Example::


        @virtual_context
        def file(name: str):
            file_ = open(name, "r")
            try:
                yield file_
            finally:
                file_.close()


        with file("dontreadthis.txt") as f:
            print(f.read()


        @virtual_context
        async def lock(name: str):
            lock_ = locks[name]
            lock_.acquire()
            try:
                yield
            finally:
                lock_.release()


        async with lock("socket-send"):
            await socket.send("wtf")
    """
    if inspect.isasyncgenfunction(function):
        return AsyncVirtualContextManager(function)
    elif inspect.isgeneratorfunction(function):
        return VirtualContextManager(function)

    raise ValueError(
        f"@virtual_context expects a generator or async generator function, got {function!r}"
    )
