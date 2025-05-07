*********
Injection
*********

You made a great trip to this page, we almost finished!

Injection is the main purpose of this library. This is the process of making it all work and sound.

Injection can be
    Synchronous - performed by :code:`inject` function.
    Supports only synchronous dependencies and dependants.
    If any dependency or dependant is asynchronous — use :code:`ainject` instead.

    Asynchronous - performed by :code:`ainject` function.
    Supports both async and sync dependencies and dependants.
    **FunDI handles both sync and async dependencies transparently, even if they’re mixed.**


Example of synchronous injection:

.. code-block:: python

    import secrets
    from contextlib import ExitStack

    from fundi import from_, scan, inject


    def require_unique_id() -> str:
        return secrets.token_hex(12)


    def application(username: str, user_id: str = from_(require_unique_id)) -> None:
        print(f"Application started with {user_id = } and {username = }")


    with ExitStack() as stack:
        inject({"username": "Kuyugama"}, scan(application), stack)


Example of asynchronous injection:

.. code-block:: python

    import secrets
    import asyncio
    from contextlib import AsyncExitStack

    from fundi import from_, scan, ainject


    async def require_user(username: str) -> str:
        await asyncio.sleep(0.4)  # pretend to be making web request
        return {"id": secrets.token_hex(12), "username": username}


    def application(user: dict[str, str] = from_(require_user)) -> None:
        print(f"Application started with {user['id'] = } and {user['username'] = }")


    async def main():
        async with AsyncExitStack() as stack:
            ainject({"username": "Kuyugama"}, scan(application), stack)

    if __name__ == "__main__":
        asyncio.run(main())

Example of injection that produces value:

.. code-block:: python

    import secrets
    from contextlib import ExitStack

    from fundi import scan, inject


    def require_unique_id() -> str:
        return secrets.token_hex(12)


    with ExitStack() as stack:
        user_id = inject({}, scan(require_user_id), stack)
        print("Generated user id is", user_id)

..

    The same works with asynchronous injection


Dependency parameter awareness
==============================
Sometimes dependencies need to know *where* they are being injected.

With **dependency parameter awareness**, FunDI makes the `fundi.Parameter`
object of the target parameter available for any dependency that declares:

.. code-block:: python

    from fundi import FromType, Parameter

    def dependency(param: FromType[Parameter]):
        print(param.name)        # name of the parameter being injected to
        print(param.annotation)  # expected type of the parameter
        ...

This allows you to build smarter and more reusable dependencies, such as:

- Automatically inferring names (e.g. :code:`user_id: int = from_header()` → :code:`X-User-Id` from parameter name)
- Performing type conversion or validation based on annotation

Example
-------

 .. literalinclude:: ../../examples/dependency_param_awareness.py

Summary
=======

+--------------------------------+--------------------+------------------------+
| Feature                        | :code:`inject`     | :code:`ainject`        |
+================================+====================+========================+
| Sync dependencies only         | Yes                | Yes                    |
+--------------------------------+--------------------+------------------------+
| Async dependencies             | No                 | Yes                    |
+--------------------------------+--------------------+------------------------+
| Mixed (sync + async)           | No                 | Yes                    |
+--------------------------------+--------------------+------------------------+
| Requires stack                 | :code:`ExitStack`  | :code:`AsyncExitStack` |
+--------------------------------+--------------------+------------------------+
| Dependency parameter awareness | Yes                | Yes                    |
+--------------------------------+--------------------+------------------------+
| Returns value                  | Yes                | Yes                    |
+--------------------------------+--------------------+------------------------+
