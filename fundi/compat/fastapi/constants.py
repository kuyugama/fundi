from starlette.responses import Response
from starlette.websockets import WebSocket
from starlette.background import BackgroundTasks
from starlette.requests import HTTPConnection, Request

__all__ = ["ALIAS_ALLOWED_CLASSES"]

ALIAS_ALLOWED_CLASSES = (
    Request,
    Response,
    WebSocket,
    HTTPConnection,
    BackgroundTasks,
)


METADATA_SECURITY_SCOPES = "fastapi_security_scopes"
METADATA_SCOPE_EXTRA = "scope_extra"
