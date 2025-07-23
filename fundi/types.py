import typing
import collections
import collections.abc
from dataclasses import dataclass, field

__all__ = [
    "R",
    "Parameter",
    "TypeResolver",
    "CallableInfo",
    "InjectionTrace",
    "ParameterResult",
    "DependencyConfiguration",
]

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
    annotation: typing.Any
    from_: "CallableInfo[typing.Any] | None"
    default: typing.Any = None
    has_default: bool = False
    resolve_by_type: bool = False
    positional_only: bool = False
    keyword_only: bool = False
    positional_varying: bool = False
    keyword_varying: bool = False


@dataclass
class CallableInfo(typing.Generic[R]):
    call: typing.Callable[..., R]
    use_cache: bool
    async_: bool
    context: bool
    generator: bool
    parameters: list[Parameter]
    return_annotation: typing.Any
    configuration: "DependencyConfiguration | None"
    named_parameters: dict[str, Parameter] = field(init=False)

    def __post_init__(self):
        self.named_parameters = {p.name: p for p in self.parameters}

    def _build_values(
        self,
        args: tuple[typing.Any, ...],
        kwargs: collections.abc.MutableMapping[str, typing.Any],
        partial: bool = False,
    ) -> dict[str, typing.Any]:
        values: dict[str, typing.Any] = {}

        args_amount = len(args)

        ix = 0
        for parameter in self.parameters:
            name = parameter.name

            if parameter.keyword_varying:
                values[name] = kwargs
                continue

            if name in kwargs:
                values[name] = kwargs.pop(name)
                continue

            if parameter.positional_varying:
                values[name] = args[ix:]
                ix = args_amount
                continue

            if ix < args_amount:
                values[name] = args[ix]
                ix += 1
                continue

            if parameter.has_default:
                values[name] = parameter.default
                continue

            if not partial:
                raise ValueError(f'Argument for parameter "{parameter.name}" not found')

        return values

    def build_values(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> collections.abc.Mapping[str, typing.Any]:
        return self._build_values(args, kwargs)

    def partial_build_values(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> collections.abc.Mapping[str, typing.Any]:
        return self._build_values(args, kwargs, partial=True)

    def build_arguments(
        self, values: collections.abc.Mapping[str, typing.Any]
    ) -> tuple[tuple[typing.Any, ...], dict[str, typing.Any]]:
        positional: tuple[typing.Any, ...] = ()
        keyword: dict[str, typing.Any] = {}

        for name, value in values.items():
            if name not in self.named_parameters:
                raise ValueError(f'Parameter named "{name}" not found')

            parameter = self.named_parameters[name]

            if parameter.positional_only:
                positional += (value,)
            elif parameter.positional_varying:
                positional += value
            elif parameter.keyword_only:
                keyword[name] = value
            elif parameter.keyword_varying:
                keyword.update(value)
            else:
                positional += (value,)

        return positional, keyword


@dataclass
class ParameterResult:
    parameter: Parameter
    value: typing.Any | None
    dependency: CallableInfo[typing.Any] | None
    resolved: bool


@dataclass
class InjectionTrace:
    info: CallableInfo[typing.Any]
    values: collections.abc.Mapping[str, typing.Any]
    origin: "InjectionTrace | None" = None


@dataclass
class DependencyConfiguration:
    configurator: CallableInfo[typing.Any]
    values: collections.abc.Mapping[str, typing.Any]
