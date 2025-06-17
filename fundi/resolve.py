import typing
import collections.abc

from fundi.util import normalize_annotation
from fundi.types import CallableInfo, ParameterResult, Parameter


def resolve_by_dependency(
    param: Parameter,
    cache: collections.abc.Mapping[typing.Callable[..., typing.Any], typing.Any],
    override: collections.abc.Mapping[typing.Callable[..., typing.Any], typing.Any],
) -> ParameterResult:
    dependency = param.from_

    assert dependency is not None

    value = override.get(dependency.call)
    if value is not None:
        if isinstance(value, CallableInfo):
            return ParameterResult(
                param, None, typing.cast(CallableInfo[typing.Any], value), resolved=False
            )

        return ParameterResult(param, value, dependency, resolved=True)

    if dependency.use_cache and dependency.call in cache:
        return ParameterResult(param, cache[dependency.call], dependency, resolved=True)

    return ParameterResult(param, None, dependency, resolved=False)


def resolve_by_type(
    scope: collections.abc.Mapping[str, typing.Any], param: Parameter
) -> ParameterResult:
    type_options = normalize_annotation(param.annotation)

    for value in scope.values():
        if not isinstance(value, type_options):
            continue

        return ParameterResult(param, value, None, resolved=True)

    return ParameterResult(param, None, None, resolved=False)


def resolve(
    scope: collections.abc.Mapping[str, typing.Any],
    info: CallableInfo[typing.Any],
    cache: collections.abc.Mapping[typing.Callable[..., typing.Any], typing.Any],
    override: collections.abc.Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
) -> collections.abc.Generator[ParameterResult, None, None]:
    """
    Try to resolve values from cache or scope for callable parameters

    Recommended use case::

        values = {}
        cache = {}
        for result in resolve(scope, info, cache):
            value = result.value
            name = result.parameter_name

            if not result.resolved:
                value = inject(scope, info, stack, cache)
                cache[name] = value

            values[name] = value


    :param scope: container with contextual values
    :param info: callable information
    :param cache: solvation cache(modify it if necessary while resolving)
    :param override: override dependencies
    :return: generator with solvation results
    """
    from fundi.exceptions import ScopeValueNotFoundError

    if override is None:
        override = {}

    for parameter in info.parameters:
        if parameter.from_:
            yield resolve_by_dependency(parameter, cache, override)
            continue

        if parameter.resolve_by_type:
            result = resolve_by_type(scope, parameter)

            if result.resolved:
                yield result
                continue

        elif parameter.name in scope:
            yield ParameterResult(parameter, scope[parameter.name], None, resolved=True)
            continue

        if parameter.has_default:
            yield ParameterResult(parameter, parameter.default, None, resolved=True)
            continue

        raise ScopeValueNotFoundError(parameter.name, info)
