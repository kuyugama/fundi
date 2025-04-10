# Basic usage

# Contents:
- [Synchronous](#sync)
- [Asynchronous](#async)
- [Mixed](#mixed)

## Sync
To use FunDI in synchronous mode you need to use `inject` function and `ExitStack` class
```python
from contextlib import ExitStack

from fundi import from_, inject, scan


def require_user() -> str:
    return "user"


def application(user: str = from_(require_user)):
    print(f"Application started with {user = }")


with ExitStack() as stack:
    inject({}, scan(application), stack)
```

## Async
To use FunDI with asynchronous code - you need to use `ainject` function and `AsyncExitStack` class
```python
from contextlib import AsyncExitStack

from fundi import from_, ainject, scan


async def require_user() -> str:
    return "user"


async def application(user: str = from_(require_user)):
    print(f"Application started with {user = }")


async with AsyncExitStack() as stack:
    await ainject({}, scan(application), stack)
```

## Mixed
You can mix async and sync dependencies using `ainject` function
```python
from contextlib import AsyncExitStack

from fundi import from_, ainject, scan


def require_user() -> str:
    return "user"


async def application(user: str = from_(require_user)):
    print(f"Application started with {user = }")


async with AsyncExitStack() as stack:
    await ainject({}, scan(application), stack)
```