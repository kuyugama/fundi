import typing
import inspect
import warnings
from types import TracebackType
from contextlib import AsyncExitStack, ExitStack

from fundi.resolve import resolve
from fundi.types import CallableInfo, InjectionTrace


def _callable_str(call: typing.Callable) -> str:
    if hasattr(call, "__qualname__"):
        name = call.__qualname__
    elif hasattr(call, "__name__"):
        name = call.__name__
    else:
        name = str(call)

    module = inspect.getmodule(call)

    module_name = "<unknown>" if module is None else module.__name__

    return f"<{name} from {module_name}>"


def _add_injection_trace(
    exception: Exception, info: CallableInfo, values: typing.Mapping[str, typing.Any]
) -> None:
    setattr(
        exception,
        "__fundi_injection_trace__",
        InjectionTrace(info, values, getattr(exception, "__fundi_injection_trace__", None)),
    )


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
        generator: typing.Generator = value
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
        generator: typing.AsyncGenerator = value
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


def tree(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo,
    cache: typing.MutableMapping[typing.Callable, typing.Mapping[str, typing.Any]] | None = None,
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
        name = result.parameter.name
        value = result.value

        if not result.resolved:
            assert result.dependency is not None
            value = tree({**scope, "__fundi_parameter__": result.parameter}, result.dependency, cache)

            if result.dependency.use_cache:
                cache[result.dependency.call] = value

        values[name] = value

    return {"call": info.call, "values": values}


def order(
    scope: typing.Mapping[str, typing.Any],
    info: CallableInfo[typing.Any],
    cache: typing.MutableMapping[typing.Callable, list[typing.Callable]] | None = None,
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
            assert result.dependency is not None

            value = order(scope, result.dependency, cache)
            order_.extend(value)
            order_.append(result.dependency.call)

            if result.dependency.use_cache:
                cache[result.dependency.call] = value

    return order_
