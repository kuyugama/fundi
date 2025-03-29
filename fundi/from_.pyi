import typing
from typing import overload

from fundi.types import CallableInfo

T = typing.TypeVar("T")

@overload
def from_(dependency: type[T]) -> type[T]: ...  # type: ignore
@overload
def from_(dependency: typing.Callable[..., typing.Any]) -> CallableInfo: ...
