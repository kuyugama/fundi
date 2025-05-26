import typing
import collections.abc
from contextlib import ExitStack, AsyncExitStack

from fundi.resolve import resolve
from fundi.types import CallableInfo
from fundi.util import call_sync, call_async, add_injection_trace


def inject(
    scope: collections.abc.Mapping[str, typing.Any],
    info: CallableInfo[typing.Any],
    stack: ExitStack,
    cache: (
        collections.abc.MutableMapping[typing.Callable[..., typing.Any], typing.Any] | None
    ) = None,
    override: collections.abc.Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
) -> typing.Any:
    """
    Synchronously inject dependencies into callable.

    :param scope: container with contextual values
    :param info: callable information
    :param stack: exit stack to properly handle generator dependencies
    :param cache: dependency cache
    :param override: override dependencies
    :return: result of callable
    """
    if info.async_:
        raise RuntimeError("Cannot process async functions in synchronous injection")

    if cache is None:
        cache = {}

    values: dict[str, typing.Any] = {}
    try:
        for result in resolve(scope, info, cache, override):
            name = result.parameter.name
            value = result.value

            if not result.resolved:
                dependency = result.dependency
                assert dependency is not None

                value = inject(
                    {**scope, "__fundi_parameter__": result.parameter},
                    dependency,
                    stack,
                    cache,
                    override,
                )

                if dependency.use_cache:
                    cache[dependency.call] = value

            values[name] = value

        return call_sync(stack, info, values)

    except Exception as exc:
        add_injection_trace(exc, info, values)
        raise exc


async def ainject(
    scope: collections.abc.Mapping[str, typing.Any],
    info: CallableInfo[typing.Any],
    stack: AsyncExitStack,
    cache: (
        collections.abc.MutableMapping[typing.Callable[..., typing.Any], typing.Any] | None
    ) = None,
    override: collections.abc.Mapping[typing.Callable[..., typing.Any], typing.Any] | None = None,
) -> typing.Any:
    """
    Asynchronously inject dependencies into callable.

    :param scope: container with contextual values
    :param info: callable information
    :param stack: exit stack to properly handle generator dependencies
    :param cache: dependency cache
    :param override: override dependencies
    :return: result of callable
    """
    if cache is None:
        cache = {}

    values: dict[str, typing.Any] = {}

    try:
        for result in resolve(scope, info, cache, override):
            name = result.parameter.name
            value = result.value

            if not result.resolved:
                dependency = result.dependency
                assert dependency is not None

                value = await ainject(
                    {**scope, "__fundi_parameter__": result.parameter},
                    dependency,
                    stack,
                    cache,
                    override,
                )

                if dependency.use_cache:
                    cache[dependency.call] = value

            values[name] = value

        if not info.async_:
            return call_sync(stack, info, values)

        return await call_async(stack, info, values)
    except Exception as exc:
        add_injection_trace(exc, info, values)
        raise exc
