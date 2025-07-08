import typing
from typing import overload
from collections.abc import Awaitable, Iterable, AsyncIterable
from contextlib import AbstractAsyncContextManager, AbstractContextManager

T = typing.TypeVar("T", bound=type)
R = typing.TypeVar("R")

@overload
def from_(
    dependency: typing.Callable[..., AbstractContextManager[R]], caching: bool = True
) -> R: ...
@overload
def from_(
    dependency: typing.Callable[..., AbstractAsyncContextManager[R]], caching: bool = True
) -> R: ...
@overload
def from_(dependency: T, caching: bool = True) -> T: ...
@overload
def from_(dependency: typing.Callable[..., Iterable[R]], caching: bool = True) -> R: ...
@overload
def from_(dependency: typing.Callable[..., AsyncIterable[R]], caching: bool = True) -> R: ...
@overload
def from_(dependency: typing.Callable[..., Awaitable[R]], caching: bool = True) -> R: ...
@overload
def from_(dependency: typing.Callable[..., R], caching: bool = True) -> R: ...
