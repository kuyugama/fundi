import typing
from typing import overload

T = typing.TypeVar("T", bound=type)
R = typing.TypeVar("R")

@overload
def from_(dependency: T) -> T: ...
@overload
def from_(dependency: typing.Callable[..., typing.Generator[R, None, None]]) -> R: ...
@overload
def from_(dependency: typing.Callable[..., typing.AsyncGenerator[R, None]]) -> R: ...
@overload
def from_(dependency: typing.Callable[..., typing.Awaitable[R]]) -> R: ...
@overload
def from_(dependency: typing.Callable[..., R]) -> R: ...

