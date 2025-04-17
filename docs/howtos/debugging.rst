*********
Debugging
*********

You made it to the final chapter. You're no longer just a user — you're a practitioner of FunDI!

Testing is good, but debugging is what separates the script kiddie from the software monk

FunDI provides useful functions to help you debug and optimize your dependency injection:
    - :code:`tree` - Generates a tree that shows how dependencies will be resolved — including resolution order and value mapping.

      .. code-block:: python

        from fundi import tree, scan

        print(tree({"username": "user"}, scan(application)))

      Outputs::

        {'call': <function application at ...>, 'values': {'username': 'user', 'user': {'call': <function require_user at ...>, 'values': {'username': 'user'}}}}

      Each node contains the function being called (:code:`call`) and the values being injected into it (:code:`values`).

    - :code:`order` - generates list that contains order in which dependencies will be called.

        Note: Result does not include function that is being passed to :code:`order` function.

      .. code-block:: python

        from fundi import order, scan

        print(order({"username": "user"}, scan(application)))

      Outputs::

        [<function require_user at ...>]

      Want more details? Try :code:`tree()`. Want less pain? Good luck.
