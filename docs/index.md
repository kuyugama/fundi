# FunDI — Functional Dependency Injection for Python

FunDI — Lightweight dependency injection library. It helps inject dependencies in simple and declarative way. 

---

## 🔥 Features

- Simple syntax — define dependency with `from_()`
- Flexible dependency resolving algorithm
- Dependency overriding support
- Inspired by FastAPI dependency injection
- Built-in dependency mocking

---

## 📚 Contents

- [Installation](installation.md)
- [Basic Usage](usage.md)
- [Advanced Usage](advanced.md)
- [Testing](testing.md)

---

## 🚀 Quick Start

```python
from contextlib import ExitStack

from fundi import scan, from_, inject


def require_user():
    return "Alice"


def greet(user: str = from_(require_user)):
    print(f"Hello, {user}!")


with ExitStack() as stack:
    inject({}, scan(greet), stack)
```

---

## 🔗 Links

- [GitHub](https://github.com/kuyugama/fundi)
- [PyPI](https://pypi.org/project/fundi/)
- [Issue Tracker](https://github.com/kuyugama/fundi/issues)
