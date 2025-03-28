import typing

from fundi.types import CallableInfo, ParameterResult


def resolve(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo,
    cache: typing.Mapping[typing.Callable, typing.Any],
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
    :return: generator with solvation results
    """
    for parameter in info.parameters:
        if parameter.from_:
            dependency = parameter.from_
            call = dependency.call

            if call in cache:
                yield ParameterResult(parameter.name, cache[call], dependency, resolved=True)
            else:
                yield ParameterResult(parameter.name, None, dependency, resolved=False)
        else:
            if parameter.name not in scope:
                raise ValueError(
                    f"Cannot resolve {parameter.name} for {info.call} - Scope does not contain required value"
                )
            yield ParameterResult(parameter.name, scope[parameter.name], None, resolved=True)
