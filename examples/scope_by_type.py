from contextlib import ExitStack

from fundi import inject, scan, FromType


class Session:
    pass


def application(
    session: FromType[Session],
):
    print(f"Application started with {session = }")


with ExitStack() as stack:
    # "_" key goes to "session" parameter of application function
    inject({"_": Session()}, scan(application), stack)
