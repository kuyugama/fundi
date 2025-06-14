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


Dependency configuration
========================
When a configurable dependency is called, FunDI stores its configuration,
so third-party tools (e.g. routers, docs generators, validators) can extract the metadata.

To get configuration of already scanned(using ``fundi.scan.scan``) dependency - 
you can use ``CallableInfo.configuration`` attribute

If dependency is not scanned - use ``is_configured(call)`` function to check whether dependency is configured:

.. literalinclude:: ../../examples/configurable_check.py

And to get dependency configuration use ``get_configuration(call)``  function on dependency callable:

.. literalinclude:: ../../examples/configurable_config.py
