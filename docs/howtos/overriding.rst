**********
Overriding
**********

Overriding is the must have feature. This feature makes feel less pain while writing tests.
Overriding works seamlessly in both sync and async contexts —
allowing you to replace either dependency callables or their results during injection.

Overridden can be
    Dependency result - dependency callable would not be called. Instead - provided value would be used.

    Dependency callable - dependency callable would be overridden during injection
    and provided callable would be called instead.

Overriding result:
    :code:`override={require_user: test_user}`
    → FunDI will skip calling :code:`require_user` and use :code:`test_user` instead.

Overriding callable:
    :code:`override={require_user: scan(mock_user_func)}`
    → FunDI will call :code:`mock_user_func` instead of :code:`require_user`.

This works with both inject() and ainject().


Example of overriding dependency result:

.. code-block:: python

    from contextlib import ExitStack

    from fundi import scan, inject

    from src import application
    from src.models import User
    from src.dependencies import require_user


    test_user = User(
        id="test-id",
        username="test_user",
    )

    with ExitStack() as stack:
        inject({"username": test_user.username}, scan(application), stack, override={require_user: test_user})


Example of overriding dependency callable:

.. code-block:: python

    from contextlib import ExitStack

    from fundi import scan, inject

    from src import application
    from src.models import User
    from src.dependencies import require_user


    test_user = User(
        id="test-id",
        username="test_user",
    )


    def test_require_user() -> User:
        return test_user


    with ExitStack() as stack:
        inject({"username": test_user.username}, scan(application), stack, override={require_user: scan(test_require_user)})

