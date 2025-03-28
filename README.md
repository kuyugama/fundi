### # _FunDI_
> Solution for problem no one had before

> Fun stays for function(or for fun if you wish) and DI for Dependency Injection

This library provides fast(to write!) dependency injection and convenient(to use!) Dependency Injection 
for functional programming on python.

### No more words, let's try!

```python
from contextlib import ExitStack
from typing import Generator, Any

from fundi import from_, inject, scan

def require_database_session(database_url: str) -> Generator[str, Any]:
    print(f"Opened database session at {database_url = }")
    yield "database session"
    print("Closed database session")


def require_user(session: str = from_(require_database_session)) -> str:
    return "user"


def application(user: str = from_(require_user), session: str = from_(require_database_session)):
    print(f"Application started with {user = }")


with ExitStack() as stack:
    inject({"session_url": "postgresql://kuyugama:insecurepassword@localhost:5432/database"}, scan(application), stack)
```

### Async? YES!!!


```python
import asyncio
from contextlib import AsyncExitStack
from typing import AsyncGenerator, Any

from fundi import from_, ainject, scan

async def require_database_session(database_url: str) -> AsyncGenerator[str, Any]:
    print(f"Opened database session at {database_url = }")
    yield "database session"
    print("Closed database session")


async def require_user(session: str = from_(require_database_session)) -> str:
    return "user"


async def application(user: str = from_(require_user), session: str = from_(require_database_session)):
    print(f"Application started with {user = }")


async def main():
    with AsyncExitStack() as stack:
        await ainject({"session_url": "postgresql://kuyugama:insecurepassword@localhost:5432/database"}, scan(application), stack)


asyncio.run(main())
```


### Utilities

- `fastdi.order` - returns order in which dependencies will be resolved
- `fastdi.tree` - returns dependency resolving tree
