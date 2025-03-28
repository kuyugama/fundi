import typing
import inspect

from fastdi.types import R, CallableInfo, Parameter


def scan(call: typing.Callable[..., R]) -> CallableInfo[R]:
    """
    Get callable information
    :param call: callable to get information from
    :return: callable information
    """
    params = []

    for param in inspect.signature(call).parameters.values():
        if isinstance(param.default, CallableInfo):
            params.append(Parameter(param.name, param.annotation, param.default))
            continue

        params.append(Parameter(param.name, param.annotation, None))

    async_ = inspect.iscoroutinefunction(call) or inspect.isasyncgenfunction(call)
    generator = inspect.isgeneratorfunction(call) or inspect.isasyncgenfunction(call)

    return CallableInfo(call=call, async_=async_, generator=generator, parameters=params)
