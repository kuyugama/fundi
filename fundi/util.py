import typing
import inspect
import warnings
import collections.abc
from types import TracebackType
from contextlib import AsyncExitStack, ExitStack

from fundi.types import CallableInfo, InjectionTrace


__all__ = [
    "call_sync",
    "call_async",
    "callable_str",
    "injection_trace",
    "add_injection_trace",
]


def callable_str(call: typing.Callable[..., typing.Any]) -> str:
    if hasattr(call, "__qualname__"):
        name = call.__qualname__
    elif hasattr(call, "__name__"):
        name = call.__name__
    else:
        name = str(call)

    module = inspect.getmodule(call)

    module_name = "<unknown>" if module is None else module.__name__

    return f"<{name} from {module_name}>"


def add_injection_trace(
    exception: Exception,
    info: CallableInfo[typing.Any],
    values: collections.abc.Mapping[str, typing.Any],
) -> None:
    setattr(
        exception,
        "__fundi_injection_trace__",
        InjectionTrace(info, values, getattr(exception, "__fundi_injection_trace__", None)),
    )


def call_sync(
    stack: ExitStack | AsyncExitStack,
    info: CallableInfo[typing.Any],
    values: collections.abc.Mapping[str, typing.Any],
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
        generator: collections.abc.Generator[typing.Any, None, None] = value
        value = next(generator)

        def close_generator(
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            tb: TracebackType | None,
        ) -> bool:
            try:
                if exc_type is not None:
                    generator.throw(exc_type, exc_value, tb)
                else:
                    next(generator)
            except StopIteration:
                # DO NOT ALLOW LIFESPAN DEPENDENCIES TO IGNORE EXCEPTIONS
                return exc_type is None
            except Exception as e:
                # Do not include re-raise of this exception in traceback to make it cleaner
                if e is exc_value:
                    return False

                raise

            warnings.warn("Generator not exited", UserWarning)

            # DO NOT ALLOW LIFESPAN DEPENDENCIES TO IGNORE EXCEPTIONS
            return exc_type is None

        stack.push(close_generator)

    return value


async def call_async(
    stack: AsyncExitStack,
    info: CallableInfo[typing.Any],
    values: collections.abc.Mapping[str, typing.Any],
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
        generator: collections.abc.AsyncGenerator[typing.Any] = value
        value = await anext(generator)

        async def close_generator(
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            tb: TracebackType | None,
        ) -> bool:
            try:
                if exc_type is not None:
                    await generator.athrow(exc_type, exc_value, tb)
                else:
                    await anext(generator)
            except StopAsyncIteration:
                # DO NOT ALLOW LIFESPAN DEPENDENCIES TO IGNORE EXCEPTIONS
                return exc_type is None
            except Exception as e:
                # Do not include re-raise of this exception in traceback to make it cleaner
                if e is exc_value:
                    return False

                raise

            warnings.warn("Generator not exited", UserWarning)

            # DO NOT ALLOW LIFESPAN DEPENDENCIES TO IGNORE EXCEPTIONS
            return exc_type is None

        stack.push_async_exit(close_generator)

    else:
        value = await value

    return value


def injection_trace(exception: Exception) -> InjectionTrace:
    """
    Get injection trace from exception

    :param exception: exception to get injection trace from
    :return: injection trace
    """
    if not hasattr(exception, "__fundi_injection_trace__"):
        raise ValueError(f"Exception {exception} does not contain injection trace")

    return typing.cast(InjectionTrace, getattr(exception, "__fundi_injection_trace__"))
