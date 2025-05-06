import typing
from dataclasses import dataclass

__all__ = ["R", "TypeResolver", "Parameter", "CallableInfo", "ParameterResult", "InjectionTrace"]

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
    use_cache: bool
    async_: bool
    generator: bool
    parameters: list[Parameter]


@dataclass
class ParameterResult:
    parameter: Parameter
    value: typing.Any | None
    dependency: CallableInfo | None
    resolved: bool


@dataclass
class InjectionTrace:
    info: CallableInfo
    values: typing.Mapping[str, typing.Any]
    origin: "InjectionTrace | None" = None
