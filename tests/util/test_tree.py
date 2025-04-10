from typing import Any, AsyncGenerator

from fundi import from_, tree, scan


async def require_database_session(database_url: str) -> AsyncGenerator[str, Any]:
    print(f"Opened database session at {database_url = }")
    yield "database session"
    print("Closed database session")


async def require_user(session: str = from_(require_database_session)) -> str:
    return "user"


def application(user: str = from_(require_user), session: str = from_(require_database_session)):
    print(f"Application started with {user = }")
    yield
    print("Application stopped")


async def test_tree():
    result = tree(
        {"database_url": "postgresql://user:password@localhost:5432/database"}, scan(application)
    )

    assert result["call"] == application

    values = result["values"]

    assert values["session"] == {
        "call": require_database_session,
        "values": {"database_url": "postgresql://user:password@localhost:5432/database"},
    }

    assert values["user"] == {
        "call": require_user,
        "values": {
            "session": {
                "call": require_database_session,
                "values": {"database_url": "postgresql://user:password@localhost:5432/database"},
            }
        },
    }
