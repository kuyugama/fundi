import typing
import inspect

from fundi.types import R, CallableInfo, Parameter


def scan(call: typing.Callable[..., R]) -> CallableInfo[R]:
    """
    Get callable information
    :param call: callable to get information from
    :return: callable information
    """
    params = []

    for param in inspect.signature(call).parameters.values():
        if isinstance(param.default, CallableInfo):
            params.append(Parameter(param.name, param.annotation, from_=param.default))
            continue

        has_default = param.default is not inspect.Parameter.empty

        params.append(
            Parameter(
                param.name,
                param.annotation,
                from_=None,
                default=param.default if has_default else None,
                has_default=has_default,
            )
        )

    async_ = inspect.iscoroutinefunction(call) or inspect.isasyncgenfunction(call)
    generator = inspect.isgeneratorfunction(call) or inspect.isasyncgenfunction(call)

    return CallableInfo(call=call, async_=async_, generator=generator, parameters=params)
