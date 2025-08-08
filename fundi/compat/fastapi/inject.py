import typing
import contextlib
import collections.abc

from fundi.types import CallableInfo
from fundi.inject import injection_impl
from fundi.util import call_async, call_sync

from .metadata import get_metadata
from .constants import METADATA_SCOPE_EXTRA


async def inject(
    scope: collections.abc.Mapping[str, typing.Any],
    info: CallableInfo[typing.Any],
    stack: contextlib.AsyncExitStack,
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

    metadata = get_metadata(info)

    scope_extra: collections.abc.Mapping[str, typing.Any] = metadata.get(METADATA_SCOPE_EXTRA, {})

    if scope_extra:
        scope = {**scope, **scope_extra}

    gen = injection_impl(scope, info, cache, override)

    value: typing.Any | None = None

    try:
        while True:
            inner_scope, inner_info, more = gen.send(value)

            if more:
                value = await inject(inner_scope, inner_info, stack, cache, override)
                continue

            if info.async_:
                return await call_async(stack, inner_info, inner_scope)

            return call_sync(stack, inner_info, inner_scope)
    except Exception as exc:
        with contextlib.suppress(StopIteration):
            gen.throw(type(exc), exc, exc.__traceback__)

        raise
