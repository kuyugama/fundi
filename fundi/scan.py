import typing
import inspect

from fundi.types import R, CallableInfo, Parameter, TypeResolver


def scan(call: typing.Callable[..., R], caching: bool = True) -> CallableInfo[R]:
    """
    Get callable information

    :param call: callable to get information from
    :param caching:  whether to use cached result of this callable or not

    :return: callable information
    """
    params = []

    for param in inspect.signature(call).parameters.values():
        if isinstance(param.default, CallableInfo):
            params.append(Parameter(param.name, param.annotation, from_=param.default))
            continue

        has_default = param.default is not inspect.Parameter.empty
        resolve_by_type = False

        annotation: type = param.annotation
        if isinstance(annotation, TypeResolver):
            annotation = annotation.annotation
            resolve_by_type = True

        elif typing.get_origin(annotation) is typing.Annotated:
            args = typing.get_args(annotation)
            annotation = args[0]

            if args[1] is TypeResolver:
                resolve_by_type = True

        params.append(
            Parameter(
                param.name,
                annotation,
                from_=None,
                default=param.default if has_default else None,
                has_default=has_default,
                resolve_by_type=resolve_by_type,
            )
        )

    async_ = inspect.iscoroutinefunction(call) or inspect.isasyncgenfunction(call)
    generator = inspect.isgeneratorfunction(call) or inspect.isasyncgenfunction(call)

    return CallableInfo(
        call=call, use_cache=caching, async_=async_, generator=generator, parameters=params
    )
