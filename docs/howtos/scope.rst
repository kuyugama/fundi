*****
Scope
*****


A scope is a dictionary passed to the injector that provides runtime values to dependencies —
especially when these values cannot or should not be declared via :code:`from_()`.
This is implicit way to inject values. While scope-based injection is powerful,
overuse may lead to unclear and hard-to-debug logic.
Use it when values must come from the external runtime context —
such as user events or app state.

Most suitable use case is to pass values that are generated outside of injection,
but should be used with in it, for example - events or application state.

Dependant's parameter with no :code:`from_(...)` as default value will be resolved from the **scope**

Values from scope can be resolved either by parameter name or by parameter type.
By default - values are resolved by parameter name. To indicate,
that value should be resolved by type you need to use :code:`FromType[...]` as type annotation
and pass required type to it.

Depending on context, this lets you avoid name clashes and enforce clearer DI behavior.

  Note: In earlier versions of FunDI to resolve parameter by type :code:`from_(...)` function was used,
  still, it is supported, but deprecated behavior. And will be removed in future updates(or not). Thus,
  I'd recommend to rewrite your code to use :code:`FromType[...]` type annotation

Example of dependant that use value from scope:

.. code-block:: python

    from urllib.request import Request

    def require_user(request: Request) -> str:
        user = request.get_header("User")

        if user is None:
            raise Unauthorized()

        return user

Dependant that use value resolved by type:

.. code-block:: python

    from urllib.request import Request

    from fundi import FromType

    def require_user(req: FromType[Request]) -> str:
        user = req.get_header("User")

        if user is None:
            raise Unauthorized()

        return user


.. warning::

    If multiple values in the scope share the same type, :code:`FromType[...]` resolution
    will prioritize the first match found. Ensure your scope is clean and well-structured.

..

  With great scope comes great confusion. Use it wisely.