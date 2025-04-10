# Advanced usage

# Contents:
- [Lifespans](#lifespan)
- [Caching](#caching)
- [Scope](#scope)
- [Scope by type](#scope-by-type)


## Lifespan
Library allows to create "lifespan" dependencies that can clean-up some
resources after data they returned was used
```python
from typing import Generator
from contextlib import ExitStack

from fundi import from_, inject, scan


def require_session() -> Generator[str, None, None]:
    print("Session set-up")
    yield "session"
    print("Session clean-up")


def application(session: str = from_(require_session)):
    print(f"Application started with {session = }")


with ExitStack() as stack:
    inject({}, scan(application), stack) 
```

## Caching
Library automatically caches all dependency results, 
so you can use dependencies whether you need not bothering
about data duplicates
```python
from typing import Generator
from contextlib import ExitStack

from fundi import from_, inject, scan


class Session:
    pass


def require_session() -> Generator[Session, None, None]:
    print("Session set-up")
    yield Session()
    print("Session clean-up")

    
def intermediate_dependency(session: Session = from_(require_session)):
    return session


def application(
    session: Session = from_(require_session),
    session1: Session = from_(intermediate_dependency)
):
    assert session is session1
    print(f"Application started with {session = }")


with ExitStack() as stack:
    inject({}, scan(application), stack) 
```

## Scope
Library provides injection scope, that allows to inject values to dependencies parameters by name

```python
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
```

## Scope by type
Dependency parameters can resolve their values from scope by type using `from_`
```python
from contextlib import ExitStack

from fundi import from_, inject, scan


class Session:
    pass


def application(
    session: from_(Session),
):
    print(f"Application started with {session = }")


with ExitStack() as stack:
    # "_" key goes to "session" parameter of application function
    inject({"_": Session()}, scan(application), stack) 
```