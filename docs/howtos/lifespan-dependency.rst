*******************
Lifespan dependency
*******************

Lifespan dependencies are python generator-functions with exactly one
:code:`yield`. Lifespan dependencies are used when a resource needs
both setup and teardown — for example, opening a file, acquiring a lock, or starting a database session.

How they work
    Before :code:`yield`: setup logic - create resource, acquire locks, etc.

    At :code:`yield` - provide value to dependant.

    After :code:`yield`: teardown logic - clean up, release, close, etc.

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


When to use lifespan dependencies
=================================
- Managing connections
- Working with files that need cleanup
- Acquiring and releasing locks
- Wrapping external APIs that require setup/teardown
