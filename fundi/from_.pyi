import typing
from typing import overload

from fundi.types import TypeResolver

T = typing.TypeVar("T", bound=type)
R = typing.TypeVar("R")

@overload
def from_(dependency: T, caching: bool = True) -> T: ...
@overload
def from_(
    dependency: typing.Callable[..., typing.Generator[R, None, None]], caching: bool = True
) -> R: ...
@overload
def from_(
    dependency: typing.Callable[..., typing.AsyncGenerator[R, None]], caching: bool = True
) -> R: ...
@overload
def from_(dependency: typing.Callable[..., typing.Awaitable[R]], caching: bool = True) -> R: ...
@overload
def from_(dependency: typing.Callable[..., R], caching: bool = True) -> R: ...

FromType: typing.TypeAlias = typing.Annotated[R, TypeResolver]
