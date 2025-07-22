*******************
Lifespan dependency
*******************

Lifespan dependencies can be either:
  - A python generator-functions with exactly one ``yield``

    How they work
      Before :code:`yield`: setup logic - create resource, acquire locks, etc.

      At :code:`yield` - provide value to dependant.

      After :code:`yield`: teardown logic - clean up, release, close, etc.

  - A class that implements context manager protocol, 
    either asynchronous(``__aenter__``, ``__aexit__``) or 
    synchronous(``__enter__``, ``__exit__``)

    How they work
      ``__init__`` method may be used to define dependencies and store their values

      ``__enter__`` or ``__aenter__``: setup logic - create resource, acquire locks, etc.

      ``__exit__`` or ``__aexit__``:  teardown logic - clean up, release, close, etc.

Lifespan dependencies should be used whenever tear-down logic should take the place. 
For example, closing a file, database session or releasing a lock.

Generator-function lifespan dependency
======================================

Example of dependency that acquires lock, opens file, yields it to dependant and closes file after it was used:

.. code-block:: python

    from threading import Lock

    FILE_LOCK = Lock()
    FILE_NAME = "file.txt"

    def acquire_file():
        with FILE_LOCK:
            file = open(FILE_NAME, "w+", encoding="utf-8")
            yield file
            file.close()

..

    I explicitly call :code:`file.close()` instead of using :code:`with open(...)` to make the example:

    - More readable for Python beginners

    - Avoid nested context managers

    - Clearly show when cleanup happens

Asynchronous dependency that does the same:

.. code-block:: python

    from asyncio import Lock

    FILE_LOCK = Lock()
    FILE_NAME = "file.txt"

    async def acquire_file():
        async with FILE_LOCK:
            file = open(FILE_NAME, "w+", encoding="utf-8")
            yield file
            file.close()


Context-manager lifespan dependency
===================================

You can define lifespan dependencies using class-based 
context managers - either **synchronous** (``__enter__`` / ``__exit__``) 
or **asynchronous** (``__aenter__`` / ``__aexit__``):

.. literalinclude:: ../../examples/context_manager.py



If you want to use a function as a context manager - 
instead of writing a class - you can use a "virtual" context manager:

.. literalinclude:: ../../examples/virtual_context_manager.py
..

"Virtual" context managers are drop-in replacements for the ``contextlib``
decorators like ``@contextmanager`` and ``@asynccontextmanager``.

The **key difference** is that they **preserve function metadata**, 
making them distinguishable from regular functions during introspection.
This is essential because ``contextlib``’s context manager 
decorators **wrap your generator function** in a way that 
**makes it impossible** for FunDI to detect them as context 
managers during introspection.

To solve this, FunDI provides a built-in ``@virtual_context`` decorator.

  It automatically detects whether the function is sync or async and applies 
  the appropriate context manager under the hood.

..

  **Developer note**

  `I originally tried to support` ``contextlib``'s `context managers directly —
  but the resulting code was way too hacky for my taste 😼`

Exception awareness
===================
Lifespan dependencies aware about downstream exceptions. This means you can
catch exception that happened during injection in lifespan dependency to do additional
cleanup if exception occurred.

  Note: Even that lifespan dependency can catch exception does not mean it can ignore it.
  FunDI does not allow lifespan dependencies to ignore exceptions. So, exception will be re-raised
  even if lifespan dependency ignored it.

.. literalinclude:: ../../examples/lifespan_exception_awareness.py

When to use lifespan dependencies
=================================
- Managing connections
- Working with files that need cleanup
- Acquiring and releasing locks
- Wrapping external APIs that require setup/teardown
