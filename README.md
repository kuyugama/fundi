# # _FunDI_
> Solution for problem no one had before

> Fun stays for function(or for fun if you wish) and DI for Dependency Injection

This library provides fast(to write!) and convenient(to use!) Dependency Injection 
for functional programming on python.

### Why?  

This library was inspired by FastAPI's dependency injection. The reasons for its existence are simple:  

- **A standalone dependency injection library.** DI shouldn't be tied to a specific framework.  
- **It simplifies code writing.** Dependency injection reduces boilerplate and improves maintainability.  
- **Lack of DI libraries for functional programming in Python.** Or maybe I just didn't want to find one :3  

Let me know if you'd like any tweaks! 😃

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
    inject({"database_url": "postgresql://kuyugama:insecurepassword@localhost:5432/database"}, scan(application), stack)
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
    async with AsyncExitStack() as stack:
        await ainject({"database_url": "postgresql://kuyugama:insecurepassword@localhost:5432/database"}, scan(application), stack)


asyncio.run(main())
```

### Resolve dependencies by type
> It's simple! Use `from_` on type annotation

```python
from contextlib import ExitStack

from fundi import from_, inject, scan

class Session:
    """Database session"""

def require_user(_: from_(Session)) -> str:
    return "user"


def application(session: from_(Session), user: str = from_(require_user)):
    print(f"Application started with {user = }")
    print(f"{session = }")


with ExitStack() as stack:
    inject({"db": Session()}, scan(application), stack)
```
> Note: while resolving dependencies by type - parameter names doesn't really matter.


### Utilities

- `fundi.order` - returns order in which dependencies will be resolved
- `fundi.tree` - returns dependency resolving tree
