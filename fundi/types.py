import typing
from dataclasses import dataclass

__all__ = ["R", "TypeResolver", "Parameter", "CallableInfo", "ParameterResult"]

R = typing.TypeVar("R")


@dataclass
class TypeResolver:
    """
    Mark that tells ``fundi.scan.scan`` to set ``Parameter.resolve_by_type`` to True.

    This changes logic of ``fundi.resolve.resolve``, so it uses ``Parameter.annotation``
    to find value in scope instead of ``Parameter.name``
    """

    annotation: type


@dataclass
class Parameter:
    name: str
    annotation: type
    from_: "CallableInfo | None"
    default: typing.Any = None
    has_default: bool = False
    resolve_by_type: bool = False


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
