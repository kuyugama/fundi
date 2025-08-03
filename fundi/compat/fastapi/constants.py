from starlette.responses import Response
from starlette.websockets import WebSocket
from starlette.background import BackgroundTasks
from fastapi.security.oauth2 import SecurityScopes
from starlette.requests import HTTPConnection, Request

__all__ = ["ALIAS_ALLOWED_CLASSES"]

ALIAS_ALLOWED_CLASSES = (
    Request,
    WebSocket,
    HTTPConnection,
    Response,
    BackgroundTasks,
    SecurityScopes,
)
