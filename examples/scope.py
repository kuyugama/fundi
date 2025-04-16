from typing import Generator
from contextlib import ExitStack

from fundi import from_, inject, scan


class Session:
    pass


def require_session(database_url: str) -> Generator[Session, None, None]:
    print(f"Session set-up with {database_url = }")
    yield Session()
    print("Session clean-up")


def application(
    session: Session = from_(require_session),
):
    print(f"Application started with {session = }")


with ExitStack() as stack:
    # "database_url" key goes to "database_url" parameter of require_session function
    inject({"database_url": "url"}, scan(application), stack)
