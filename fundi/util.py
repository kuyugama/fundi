import typing
from contextlib import AsyncExitStack, ExitStack

from fastdi.resolve import resolve
from fastdi.types import CallableInfo


def _call_sync(
    stack: ExitStack | AsyncExitStack,
    info: CallableInfo[typing.Any],
    values: typing.Mapping[str, typing.Any],
) -> typing.Any:
    """
    Synchronously call dependency callable.

    :param stack: exit stack to properly handle generator dependencies
    :param info: callable information
    :param values: callable arguments
    :return: callable result
    """
    value = info.call(**values)

    if info.generator:
        generator = value
        value = next(generator)

        def exit_generator():
            try:
                next(generator)
            except StopIteration:
                pass

        stack.callback(exit_generator)

    return value


async def _call_async(
    stack: AsyncExitStack, info: CallableInfo[typing.Any], values: typing.Mapping[str, typing.Any]
) -> typing.Any:
    """
    Asynchronously call dependency callable.

    :param stack: exit stack to properly handle generator dependencies
    :param info: callable information
    :param values: callable arguments
    :return: callable result
    """
    value = info.call(**values)

    if info.generator:
        generator = value
        value = await anext(generator)

        async def exit_generator():
            try:
                await anext(generator)
            except StopAsyncIteration:
                pass

        stack.push_async_callback(exit_generator)

    else:
        value = await value

    return value


def tree(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo,
    cache: typing.Mapping[typing.Callable, typing.Mapping[str, typing.Any]] = None,
) -> typing.Mapping[str, typing.Any]:
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
        name = result.parameter_name
        value = result.value

        if not result.resolved:
            value = tree(scope, result.dependency, cache)
            cache[result.dependency.call] = value

        values[name] = value

    return {"call": info.call, "values": values}


def order(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo[typing.Any],
    cache: typing.Mapping[typing.Callable, list[typing.Callable]] = None,
) -> list[typing.Callable]:
    """
    Get resolving order of callable dependencies.

    :param info: callable information
    :param scope: container with contextual values
    :param cache: solvation cache
    :return: order of dependencies
    """
    if cache is None:
        cache = {}

    order_ = []

    for result in resolve(scope, info, cache):
        if not result.resolved:
            value = order(scope, result.dependency, cache)
            order_.extend(value)
            order_.append(result.dependency.call)
            cache[result.dependency.call] = value

    return order_
