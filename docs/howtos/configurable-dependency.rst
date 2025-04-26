********************************
Configurable dependency(factory)
********************************

FunDI supports dependency factories - functions that return other dependencies,
they are called Configurable dependencies. They can create completely different dependencies
based on parameters, or only slightly change their behavior.

.. literalinclude:: ../../examples/configurable_dependency.py

..

  Note: :code:`configurable_dependency` decorator is optional, but it caches dependencies,
  so their results can be cached on injection.

  Also, :code:`configurable_dependency` decorator does not cache dependencies configured with mutable arguments.

Composite dependencies
======================
Composite dependencies - special kind of configurable dependency that accepts other
dependencies as parameters

.. literalinclude:: ../../examples/composite_dependency.py