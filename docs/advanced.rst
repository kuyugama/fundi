**************
Advanced usage
**************

Lifespan
========
Library allows to create "lifespan" dependencies that can clean-up some
resources after data they returned was used

.. literalinclude:: ../examples/lifespan.py


Lifespan exception awareness
============================
Lifespan dependencies aware about downstream exceptions. This means you can
catch exception that happened during injection in lifespan dependency to do additional
cleanup if exception occurred.

  Note: Even that lifespan dependency can catch exception does not mean it can ignore it.
  FunDI does not allow lifespan dependencies to ignore exceptions. So, exception will be re-raised
  even if lifespan dependency ignored it.

.. literalinclude:: ../examples/lifespan_exception_awareness.py

Caching
=======
FunDI caches dependency results by default — so each dependency is
only evaluated once per injection cycle, avoiding duplicate work or inconsistent data.

.. literalinclude:: ../examples/caching.py

To disable this behavior - use :code:`caching=False` parameter when defining dependant's dependency:

.. literalinclude:: ../examples/disabled_caching.py

Scope
=====
Library provides injection scope, that allows to inject values to dependencies parameters by name

.. literalinclude:: ../examples/scope.py

Dependency parameter awareness
==============================
Dependant's dependencies know of the parameter they are injected to.

..

  Note:
  Parameter-aware dependencies are cached just like any other dependency by default.

  This means that even if the same function is injected into multiple parameters
  (e.g., :code:`user_id`, :code:`client_id`), it will only be called once, and the cached
  result will be reused — regardless of which parameter it's injected into.

  If your function depends on the parameter name or annotation (e.g. to extract different headers),
  you must disable caching manually using :code:`from_(..., caching=False)`.

  This behavior is intentional for now and may change in future versions,
  but currently it's the developer’s responsibility to manage it.


This can be used to create more transparent dependencies:

 .. literalinclude:: ../examples/dependency_param_awareness.py


Scope by type
=============
Dependency parameters can resolve their values from scope by type using `from_`

.. literalinclude:: ../examples/scope_by_type.py


Exception tracing
=================
FunDI adds injection trace to all exceptions on injection to help you understand them

.. literalinclude:: ../examples/exception_tracing.py


Configurable dependencies
=========================
FunDI supports configurable dependencies - functions that return dependencies with different behavior
based on provided arguments to them:

.. literalinclude:: ../examples/configurable_dependency.py

..

  Note: :code:`configurable_dependency` decorator is optional, but it caches dependencies,
  so their results can be cached on injection.

  Also, :code:`configurable_dependency` decorator does not cache dependencies configured with mutable arguments.

To get configuration of already scanned(using ``fundi.scan.scan``) dependency - 
you can use ``CallableInfo.configuration`` attribute

If dependency is not scanned - use ``is_configured(call)`` function to check whether dependency is configured:

.. literalinclude:: ../examples/configurable_check.py

And to get dependency configuration use ``get_configuration(call)``  function on dependency callable:

.. literalinclude:: ../examples/configurable_config.py


Composite dependencies
======================
Composite dependencies - special kind of configurable dependency that accepts other
dependencies as parameters

.. literalinclude:: ../examples/composite_dependency.py
