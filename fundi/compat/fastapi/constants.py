from starlette.responses import Response
from starlette.websockets import WebSocket
from starlette.background import BackgroundTasks
from starlette.requests import HTTPConnection, Request

__all__ = ["ALIAS_ALLOWED_CLASSES"]

ALIAS_ALLOWED_CLASSES = (
    WebSocket,
    Request,
    Response,
    HTTPConnection,
    BackgroundTasks,
)


METADATA_SECURITY_SCOPES = "fastapi_security_scopes"
METADATA_DEPENDANT = "fastapi_dependant"
METADATA_SCOPE_EXTRA = "scope_extra"
METADATA_ALIASES = "fastapi_aliases"
