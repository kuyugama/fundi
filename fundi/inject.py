import typing
from contextlib import ExitStack, AsyncExitStack

from fundi.resolve import resolve
from fundi.types import CallableInfo
from fundi.util import _call_sync, _call_async


def inject(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo[typing.Any],
    stack: ExitStack,
    cache: typing.Mapping[typing.Callable, typing.Any] = None,
) -> typing.Any:
    """
    Synchronously inject dependencies into callable.

    :param scope: container with contextual values
    :param info: callable information
    :param stack: exit stack to properly handle generator dependencies
    :param cache: dependency cache
    :return: result of callable
    """
    if info.async_:
        raise RuntimeError("Cannot process async functions in synchronous injection")

    if cache is None:
        cache = {}

    values = {}

    for result in resolve(scope, info, cache):
        name = result.parameter_name
        value = result.value

        if not result.resolved:
            dependency = result.dependency

            value = inject(scope, dependency, stack, cache)
            cache[dependency.call] = value

        values[name] = value

    return _call_sync(stack, info, values)


async def ainject(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo[typing.Any],
    stack: AsyncExitStack,
    cache: typing.Mapping[typing.Callable, typing.Any] = None,
) -> typing.Any:
    """
    Asynchronously inject dependencies into callable.

    :param scope: container with contextual values
    :param info: callable information
    :param stack: exit stack to properly handle generator dependencies
    :param cache: dependency cache
    :return: result of callable
    """
    if cache is None:
        cache = {}

    values = {}

    for result in resolve(scope, info, cache):
        name = result.parameter_name
        value = result.value

        if not result.resolved:
            dependency = result.dependency

            value = await ainject(scope, dependency, stack, cache)
            cache[dependency.call] = value

        values[name] = value

    if not info.async_:
        return _call_sync(stack, info, values)

    return await _call_async(stack, info, values)
