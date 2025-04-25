********************************
Configurable dependency(factory)
********************************

FunDI supports dependency factories - functions that return other dependencies,
they are called Configurable dependencies. They can create completely different dependencies
based on parameters, or only slightly change their behavior.

.. literalinclude:: ../../examples/configurable_dependency.py

..

  Note: :code:`configurable_dependency` decorator is optional, but it caches dependencies,
  so they results can be cached on injection.

Composite dependencies
======================
Composite dependencies - special kind of configurable dependency that accepts other
dependencies as parameters

.. literalinclude:: ../../examples/composite_dependency.py