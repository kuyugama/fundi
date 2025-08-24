import typing
from typing import overload
from collections.abc import Generator, AsyncGenerator, Awaitable, Sequence
from contextlib import AbstractAsyncContextManager, AbstractContextManager

R = typing.TypeVar("R")

@overload
def secured(
    dependency: typing.Callable[..., AbstractContextManager[R]],
    scopes: Sequence[str],
    caching: bool = True,
) -> R: ...
@overload
def secured(
    dependency: typing.Callable[..., AbstractAsyncContextManager[R]],
    scopes: Sequence[str],
    caching: bool = True,
) -> R: ...
@overload
def secured(
    dependency: typing.Callable[..., Generator[R, None, None]],
    scopes: Sequence[str],
    caching: bool = True,
) -> R: ...
@overload
def secured(
    dependency: typing.Callable[..., AsyncGenerator[R, None]],
    scopes: Sequence[str],
    caching: bool = True,
) -> R: ...
@overload
def secured(
    dependency: typing.Callable[..., Awaitable[R]], scopes: Sequence[str], caching: bool = True
) -> R: ...
@overload
def secured(
    dependency: typing.Callable[..., R], scopes: Sequence[str], caching: bool = True
) -> R: ...
