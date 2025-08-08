import typing
from collections import defaultdict


from starlette.responses import Response
from starlette.websockets import WebSocket
from starlette.background import BackgroundTasks
from pydantic.v1.utils import lenient_issubclass
from starlette.requests import HTTPConnection, Request

from fundi.types import CallableInfo
from .constants import ALIAS_ALLOWED_CLASSES


def get_request_related_aliases(ci: CallableInfo[typing.Any]) -> dict[type, set[str]]:
    aliases: defaultdict[type, set[str]] = defaultdict(set)
    for parameter in ci.parameters:
        if parameter.from_ is not None:
            subaliases = get_request_related_aliases(parameter.from_)
            for type_, aliases_ in subaliases.items():
                aliases[type_].update(aliases_)
            continue

        origin = typing.get_origin(parameter.annotation) or parameter.annotation

        for type_ in ALIAS_ALLOWED_CLASSES:
            if lenient_issubclass(origin, type_):
                aliases[type_].add(parameter.name)
    return aliases


def resolve_aliases(
    scope_aliases: dict[type, set[str]],
    request: Request,
    background_tasks: BackgroundTasks,
    response: Response,
) -> dict[str, typing.Any]:
    values: dict[str, typing.Any] = {}

    for type_, names in scope_aliases.items():
        if type_ is HTTPConnection:
            value = request
        elif type_ is Request:
            value = request
        elif type_ is WebSocket:
            assert isinstance(request, WebSocket), "Not a websocket"
            value = request
        elif type_ is BackgroundTasks:
            value = background_tasks
        elif type_ is Response:
            value = response
        else:
            raise RuntimeError(f"Unsupported alias type {type_!r}")

        values.update({name: value for name in names})

    return values
