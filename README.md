# # _FunDI_
> Solution for problem no one had before

> Fun stays for function(or for fun if you wish) and DI for Dependency Injection

This library provides fast(to write!) and convenient(to use!) Dependency Injection 
for functional programming on python.

## Why?  

This library was inspired by FastAPI's dependency injection. The reasons for its existence are simple:  

- **A standalone dependency injection library.** DI shouldn't be tied to a specific framework.  
- **It simplifies code writing.** Dependency injection reduces boilerplate and improves maintainability.  
- **Lack of DI libraries for functional programming in Python.** Or maybe I just didn't want to find one :3  


## No more words, let's try!

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

See the documentation to get more examples: https://fundi.readthedocs.io/en/latest/

### Component explanation:
- `fundi.from_` - Helps define dependencies.

  Use cases:
    - Tell resolver to resolve parameter value by its type, not name (ex: `parameter: from_(Session)`)
    - Define dependency (ex: `parameter: type = from_(dependency)`).

      In this case it can be replaced with `fundi.scan.scan` (ex: `parameter: type = scan(dependency)`)
- `fundi.scan` - Scans function for dependencies. Returns `CallableInfo` object that is 
  used by all functions that resolve dependencies.
- `fundi.order` - returns order in which dependencies will be resolved
- `fundi.tree` - returns dependency resolving tree
