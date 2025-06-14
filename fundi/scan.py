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
    params: list[Parameter] = []
    signature = inspect.signature(call)

    for param in signature.parameters.values():
        positional_only = param.kind == inspect.Parameter.POSITIONAL_ONLY
        keyword_only = param.kind == inspect.Parameter.KEYWORD_ONLY
        if isinstance(param.default, CallableInfo):
            params.append(
                Parameter(
                    param.name,
                    param.annotation,
                    from_=typing.cast(CallableInfo[typing.Any], param.default),
                    positional_only=positional_only,
                    keyword_only=keyword_only,
                )
            )
            continue

        has_default = param.default is not inspect.Parameter.empty
        resolve_by_type = False

        annotation = param.annotation
        if isinstance(annotation, TypeResolver):
            annotation = annotation.annotation
            resolve_by_type = True

        elif typing.get_origin(annotation) is typing.Annotated:
            args = typing.get_args(annotation)

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
                positional_only=positional_only,
                keyword_only=keyword_only,
            )
        )

    async_: bool = inspect.iscoroutinefunction(call) or inspect.isasyncgenfunction(call)
    generator: bool = inspect.isgeneratorfunction(call) or inspect.isasyncgenfunction(call)

    info = typing.cast(
        CallableInfo[R],
        CallableInfo(
            call=call,
            use_cache=caching,
            async_=async_,
            generator=generator,
            parameters=params,
            return_annotation=signature.return_annotation,
        ),
    )

    return info
