******************************
Compare with DIs in frameworks
******************************

Aiogram
=======
Implicit VS explicit

Aiogram's Dependency Injection makes injection in implicit way - they are created outside of
handler context, so it is hard to tell where values came from. Also, to make it create
only required values you need to do more work using
`flags <https://docs.aiogram.dev/en/latest/dispatcher/flags.html>`_, including validating & handling these
flags all by yourself. The more your project grow, the more this abstraction leads to unclear, harder-to-debug code.

Let's take a look:

.. code-block:: python

    from aiogram import Router, F
    from aiogram.types import Message

    from src.models import User


    router = Router()

    @router.message(F.text = "/whoami", flags={"requires": {User: "user"}})
    async def on_whoami(message: Message, user: User):
        pass

This code shows problem in detail:
I can't tell where parameter :code:`user` is created, neither is it created properly.
Also, I can set any values into flags and get no error at bot start.

How this looks with FunDI:

.. code-block:: python

    from fundi import from_

    from src.models import User
    from src.dependencies import require_user

    async def on_whoami(user: User = from_(require_user)):
        pass

FunDI makes it clearer. You can understand from where values came and where they are created.
No flags, no implicit injection.

Yes, FunDI also supports implicit injection with :code:`scope`. But also makes it much easier to debug
because, it tells you which function from which module requires value that was not passed to scope.

FastAPI
=======
Request dependent VS fully independent

FunDI is similar to FastAPI's Dependency Injection(because it was inspired by FastAPI).
It has only one problem - you can't use it outside of Request scope. FunDI was created to
cover this issue and successfully does this job.


Summary
=======
+-------------+------------+---------+-----------+
|   Is        | FunDI      | Aiogram | FastAPI   |
+=============+============+=========+===========+
| Implicit    | Optionally |   Yes   | Partially |
+-------------+------------+---------+-----------+
| Independent |     Yes    |    No   |     No    |
+-------------+------------+---------+-----------+
