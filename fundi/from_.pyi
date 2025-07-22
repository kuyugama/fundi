import typing
from typing import overload
from collections.abc import Generator, AsyncGenerator, Awaitable

T = typing.TypeVar("T", bound=type)
R = typing.TypeVar("R")

@overload
def from_(dependency: T, caching: bool = True) -> T: ...
@overload
def from_(
    dependency: typing.Callable[..., Generator[R, None, None]], caching: bool = True
) -> R: ...
@overload
def from_(dependency: typing.Callable[..., AsyncGenerator[R, None]], caching: bool = True) -> R: ...
@overload
def from_(dependency: typing.Callable[..., Awaitable[R]], caching: bool = True) -> R: ...
@overload
def from_(dependency: typing.Callable[..., R], caching: bool = True) -> R: ...
