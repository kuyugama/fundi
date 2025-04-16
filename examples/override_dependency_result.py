from contextlib import ExitStack

from fundi import from_, inject, scan


def require_user() -> str:
    return "user"


def application(user: str = from_(require_user)):
    print(f"Application started with {user = }")


with ExitStack() as stack:
    inject({}, scan(application), stack, override={require_user: "test_user"})
