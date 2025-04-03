import inspect
import typing

from fundi.types import CallableInfo, ParameterResult


def resolve_by_dependency(
    name: str, dependency: CallableInfo, cache: typing.Mapping[typing.Callable, typing.Any], override: typing.Mapping[typing.Callable, typing.Any]
) -> ParameterResult:
    call = dependency.call

    if call in override:
        return ParameterResult(name, override[call], dependency, resolved=True)

    if call in cache:
        return ParameterResult(name, cache[call], dependency, resolved=True)

    return ParameterResult(name, None, dependency, resolved=False)


def resolve_by_type(
    scope: typing.Mapping[str, typing.Any], name: str, annotation: type
) -> ParameterResult:
    type_options = (annotation,)

    origin = typing.get_origin(annotation)
    if origin is typing.Union:
        type_options = tuple(t for t in typing.get_args(annotation) if t is not None)
    elif origin is not None:
        type_options = (origin,)

    for value in scope.values():
        if not isinstance(value, type_options):
            continue

        return ParameterResult(name, value, None, resolved=True)

    return ParameterResult(name, None, None, resolved=False)


def resolve(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo,
    cache: typing.Mapping[typing.Callable, typing.Any],
    override: typing.Mapping[typing.Callable, typing.Any] = None,
) -> typing.Generator[ParameterResult, None, None]:
    """
    Try to resolve values from cache or scope for callable parameters

    Recommended use case:

    Example::

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
    if override is None:
        override = {}

    module = inspect.getmodule(info.call)
    module_name = module.__name__ if module else "<unknown module>"
    for parameter in info.parameters:
        if parameter.from_:
            yield resolve_by_dependency(parameter.name, parameter.from_, cache, override)
            continue

        if parameter.resolve_by_type:
            result = resolve_by_type(scope, parameter.name, parameter.annotation)

            if result.resolved:
                yield result
                continue

        elif parameter.name in scope:
            yield ParameterResult(parameter.name, scope[parameter.name], None, resolved=True)
            continue

        if parameter.has_default:
            yield ParameterResult(parameter.name, parameter.default, None, resolved=True)
            continue

        raise ValueError(
            f"Cannot resolve {parameter.name} for {info.call} from {module_name} - Scope does not contain required value"
        )
