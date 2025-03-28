import typing
from dataclasses import dataclass

__all__ = ["R", "Parameter", "CallableInfo", "ParameterResult"]

R = typing.TypeVar("R")


@dataclass
class Parameter:
    name: str
    annotation: type
    from_: "CallableInfo | None"
    default: typing.Any = None
    has_default: bool = False


@dataclass
class CallableInfo(typing.Generic[R]):
    call: typing.Callable[..., typing.Any]
    async_: bool
    generator: bool
    parameters: list[Parameter]


@dataclass
class ParameterResult:
    parameter_name: str
    value: typing.Any | None
    dependency: CallableInfo | None
    resolved: bool
