from dataclasses import replace
import typing
import inspect

from fundi.util import is_configured, get_configuration
from fundi.types import R, CallableInfo, Parameter, TypeResolver


def _transform_parameter(parameter: inspect.Parameter) -> Parameter:
    positional_only = parameter.kind == inspect.Parameter.POSITIONAL_ONLY
    keyword_only = parameter.kind == inspect.Parameter.KEYWORD_ONLY

    if isinstance(parameter.default, CallableInfo):
        return Parameter(
            parameter.name,
            parameter.annotation,
            from_=typing.cast(CallableInfo[typing.Any], parameter.default),
            positional_only=positional_only,
            keyword_only=keyword_only,
        )

    has_default = parameter.default is not inspect.Parameter.empty
    resolve_by_type = False

    annotation = parameter.annotation
    if isinstance(annotation, TypeResolver):
        annotation = annotation.annotation
        resolve_by_type = True

    elif typing.get_origin(annotation) is typing.Annotated:
        args = typing.get_args(annotation)

        if args[1] is TypeResolver:
            resolve_by_type = True

    return Parameter(
        parameter.name,
        annotation,
        from_=None,
        default=parameter.default if has_default else None,
        has_default=has_default,
        resolve_by_type=resolve_by_type,
        positional_only=positional_only,
        keyword_only=keyword_only,
    )


def scan(call: typing.Callable[..., R], caching: bool = True) -> CallableInfo[R]:
    """
    Get callable information

    :param call: callable to get information from
    :param caching:  whether to use cached result of this callable or not

    :return: callable information
    """

    if hasattr(call, "__fundi_info__"):
        info = typing.cast(CallableInfo[typing.Any], getattr(call, "__fundi_info__"))
        return replace(info, use_cache=caching)

    signature = inspect.signature(call)

    generator = inspect.isgeneratorfunction(call)
    async_generator = inspect.isasyncgenfunction(call)

    context = hasattr(call, "__enter__") and hasattr(call, "__exit__")
    async_context = hasattr(call, "__aenter__") and hasattr(call, "__aexit__")

    async_ = inspect.iscoroutinefunction(call) or async_generator or async_context
    generator = generator or async_generator
    context = context or async_context

    parameters = [_transform_parameter(parameter) for parameter in signature.parameters.values()]

    info = typing.cast(
        CallableInfo[R],
        CallableInfo(
            call=call,
            use_cache=caching,
            async_=async_,
            context=context,
            generator=generator,
            parameters=parameters,
            return_annotation=signature.return_annotation,
            configuration=get_configuration(call) if is_configured(call) else None,
        ),
    )

    try:
        setattr(call, "__fundi_info__", info)
    except (AttributeError, TypeError):
        pass

    return info
