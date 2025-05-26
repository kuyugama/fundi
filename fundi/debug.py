import typing
import collections.abc

from fundi.resolve import resolve
from fundi.types import CallableInfo


def tree(
    scope: collections.abc.Mapping[str, typing.Any],
    info: CallableInfo[typing.Any],
    cache: (
        collections.abc.MutableMapping[
            typing.Callable[..., typing.Any], collections.abc.Mapping[str, typing.Any]
        ]
        | None
    ) = None,
) -> collections.abc.Mapping[str, typing.Any]:
    """
    Get tree of dependencies of callable.

    :param scope: container with contextual values
    :param info: callable information
    :param cache: tree generation cache
    :return: Tree of dependencies
    """
    if cache is None:
        cache = {}

    values = {}

    for result in resolve(scope, info, cache):
        name = result.parameter.name
        value = result.value

        if not result.resolved:
            dependency = result.dependency
            assert dependency is not None
            value = tree({**scope, "__fundi_parameter__": result.parameter}, dependency, cache)

            if dependency.use_cache:
                cache[dependency.call] = value

        values[name] = value

    return {"call": info.call, "values": values}


def order(
    scope: collections.abc.Mapping[str, typing.Any],
    info: CallableInfo[typing.Any],
    cache: (
        collections.abc.MutableMapping[
            typing.Callable[..., typing.Any], list[typing.Callable[..., typing.Any]]
        ]
        | None
    ) = None,
) -> list[typing.Callable[..., typing.Any]]:
    """
    Get resolving order of callable dependencies.

    :param info: callable information
    :param scope: container with contextual values
    :param cache: solvation cache
    :return: order of dependencies
    """
    if cache is None:
        cache = {}

    order_: list[typing.Callable[..., typing.Any]] = []

    for result in resolve(scope, info, cache):
        if not result.resolved:
            assert result.dependency is not None

            value = order(scope, result.dependency, cache)
            order_.extend(value)
            order_.append(result.dependency.call)

            if result.dependency.use_cache:
                cache[result.dependency.call] = value

    return order_
