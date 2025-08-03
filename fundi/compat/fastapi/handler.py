import json
import typing
from collections.abc import Coroutine
from contextlib import AsyncExitStack

from fastapi import params
from fastapi.types import IncEx
from pydantic.v1.fields import Undefined
from starlette.websockets import WebSocket
from fastapi.routing import serialize_response
from starlette.exceptions import HTTPException
from starlette.background import BackgroundTasks
from fastapi.dependencies.models import Dependant
from fastapi.exceptions import RequestValidationError
from starlette.requests import HTTPConnection, Request
from starlette.responses import JSONResponse, Response
from fastapi.dependencies.utils import solve_dependencies
from fastapi.utils import is_body_allowed_for_status_code
from fastapi._compat import ModelField, _normalize_errors  # pyright: ignore[reportPrivateUsage]
from fastapi.datastructures import Default, DefaultPlaceholder

from fundi.inject import ainject
from fundi.types import CallableInfo


async def validate_body(request: Request, stack: AsyncExitStack, body_field: ModelField | None):
    is_body_form = body_field and isinstance(body_field.field_info, params.Form)
    try:
        if body_field:
            if is_body_form:
                form = await request.form()
                stack.push_async_callback(form.close)
                return form

            body_bytes = await request.body()
            if body_bytes:
                json_body: typing.Any = Undefined
                content_type_value = request.headers.get("content-type")

                if not content_type_value:
                    json_body = await request.json()

                else:
                    if content_type_value.count("/") != 1:
                        content_type_value = "text/plain"

                    maintype, subtype = content_type_value.split("/", 1)

                    if maintype == "application":
                        if subtype == "json" or subtype.endswith("+json"):
                            json_body = await request.json()

                if json_body != Undefined:
                    return json_body
                else:
                    return typing.cast(typing.Any, body_bytes)
    except json.JSONDecodeError as e:
        validation_error = RequestValidationError(
            [
                {
                    "type": "json_invalid",
                    "loc": ("body", e.pos),
                    "msg": "JSON decode error",
                    "input": {},
                    "ctx": {"error": e.msg},
                }
            ],
            body=e.doc,
        )
        raise validation_error from e
    except HTTPException:
        # If a middleware raises an HTTPException, it should be raised again
        raise
    except Exception as e:
        http_error = HTTPException(status_code=400, detail="There was an error parsing the body")
        raise http_error from e


def get_request_handler(
    ci: CallableInfo[typing.Any],
    scope_dependant: Dependant,
    extra_dependencies: list[CallableInfo[typing.Any]],
    scope_aliases: dict[type, set[str]],
    body_field: ModelField | None = None,
    status_code: int | None = None,
    response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse),
    response_field: ModelField | None = None,
    response_model_include: IncEx | None = None,
    response_model_exclude: IncEx | None = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    dependency_overrides_provider: typing.Any | None = None,
    embed_body_fields: bool = False,
) -> typing.Callable[[Request], Coroutine[typing.Any, typing.Any, Response]]:

    if isinstance(response_class, DefaultPlaceholder):
        actual_response_class: type[Response] = response_class.value
    else:
        actual_response_class = response_class

    async def app(request: Request) -> Response:
        async with AsyncExitStack() as stack:
            body = await validate_body(request, stack, body_field)

            scope = await solve_dependencies(
                request=request,
                dependant=scope_dependant,
                body=body,
                dependency_overrides_provider=dependency_overrides_provider,
                async_exit_stack=stack,
                embed_body_fields=embed_body_fields,
            )

            if scope.errors:
                raise RequestValidationError(_normalize_errors(scope.errors), body=body)

            values = {**scope.values}

            for type_, names in scope_aliases.items():

                if type_ is HTTPConnection:
                    value = request
                elif type_ is Request:
                    value = request
                elif type_ is WebSocket:
                    assert isinstance(request, WebSocket), "Not a websocket"
                    value = request
                elif type_ is BackgroundTasks:
                    value = scope.background_tasks or BackgroundTasks()
                elif type_ is Response:
                    value = scope.response
                else:
                    value = scope_dependant.security_scopes

                values.update({name: value for name in names})

            for dependency in extra_dependencies:
                await ainject(values, dependency, stack)

            raw_response = await ainject(values, ci, stack)

            if isinstance(raw_response, Response):
                if raw_response.background is None:
                    raw_response.background = scope.background_tasks

                response = raw_response
            else:
                response_args: dict[str, typing.Any] = {"background": scope.background_tasks}

                # If status_code was set, use it, otherwise use the default from the
                # response class, in the case of redirect it's 307

                status = scope.response.status_code or status_code
                if status is not None:
                    response_args["status_code"] = status

                content = await serialize_response(
                    field=response_field,
                    response_content=raw_response,
                    include=response_model_include,
                    exclude=response_model_exclude,
                    by_alias=response_model_by_alias,
                    exclude_unset=response_model_exclude_unset,
                    exclude_defaults=response_model_exclude_defaults,
                    exclude_none=response_model_exclude_none,
                    is_coroutine=ci.async_,
                )
                response = actual_response_class(content, **response_args)
                if not is_body_allowed_for_status_code(response.status_code):
                    response.body = b""

                response.headers.raw.extend(scope.response.headers.raw)

        return response

    return app
