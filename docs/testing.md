# Testing

# Contents:
- [Override dependency results](#dependency-result-overriding)
- [Override dependencies](#dependency-overriding)


## Dependency result overriding
```python
from contextlib import ExitStack

from fundi import from_, inject, scan


def require_user() -> str:
    return "user"


def application(user: str = from_(require_user)):
    print(f"Application started with {user = }")


with ExitStack() as stack:
    inject({}, scan(application), stack, override={require_user: "test_user"})
```

## Dependency overriding
```python
from contextlib import ExitStack

from fundi import from_, inject, scan


def require_user() -> str:
    return "user"


def test_require_user() -> str:
    return "custom_user_from_dependency"


def application(user: str = from_(require_user)):
    print(f"Application started with {user = }")


with ExitStack() as stack:
    inject({}, scan(application), stack, override={require_user: scan(test_require_user)})
```