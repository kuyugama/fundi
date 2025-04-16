import asyncio
from contextlib import AsyncExitStack

from fundi import from_, ainject, scan


def require_user() -> str:
    return "user"


async def application(user: str = from_(require_user)):
    print(f"Application started with {user = }")


async def main():
    async with AsyncExitStack() as stack:
        await ainject({}, scan(application), stack)


if __name__ == "__main__":
    asyncio.run(main())
