import typing
from contextlib import ExitStack

from fundi import from_, scan, inject, configurable_dependency


def require_user() -> dict[str, str | tuple[str]]:
    return {"username": "Kuyugama", "permissions": ("catch-apple",)}


@configurable_dependency
def require_permission(
    permission: str,
    user_resolver: typing.Callable[..., typing.Mapping[str, str | tuple[str]]] = require_user,
):
    def checker(user: typing.Mapping[str, str | tuple[str]] = from_(user_resolver)) -> None:
        if permission not in user["permissions"]:
            raise PermissionError(permission)

    return checker


def application(
    _=from_(require_permission("catch-apple")),
):
    print("User has permission")


with ExitStack() as stack:
    inject({}, scan(application), stack)
