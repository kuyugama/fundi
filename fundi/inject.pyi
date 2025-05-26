import typing
from typing import overload
from contextlib import ExitStack as SyncExitStack, AsyncExitStack
from collections.abc import Generator, AsyncGenerator, Mapping, Awaitable

from fundi.types import CallableInfo

R = typing.TypeVar("R")

ExitStack = AsyncExitStack | SyncExitStack

@overload
def inject(
    scope: Mapping[str, typing.Any],
    info: CallableInfo[Generator[R, None, None]],
    stack: ExitStack,
    cache: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
    override: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
) -> R: ...
@overload
def inject(
    scope: Mapping[str, typing.Any],
    info: CallableInfo[R],
    stack: ExitStack,
    cache: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
    override: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
) -> R: ...
@overload
async def ainject(
    scope: Mapping[str, typing.Any],
    info: CallableInfo[Generator[R, None, None]],
    stack: AsyncExitStack,
    cache: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
    override: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
) -> R: ...
@overload
async def ainject(
    scope: Mapping[str, typing.Any],
    info: CallableInfo[AsyncGenerator[R, None]],
    stack: AsyncExitStack,
    cache: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
    override: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
) -> R: ...
@overload
async def ainject(
    scope: Mapping[str, typing.Any],
    info: CallableInfo[Awaitable[R]],
    stack: AsyncExitStack,
    cache: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
    override: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
) -> R: ...
@overload
async def ainject(
    scope: Mapping[str, typing.Any],
    info: CallableInfo[R],
    stack: AsyncExitStack,
    cache: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
    override: Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
) -> R: ...
