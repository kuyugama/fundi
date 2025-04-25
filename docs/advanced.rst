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


Composite dependencies
======================
Composite dependencies - special kind of configurable dependency that accepts other
dependencies as parameters

.. literalinclude:: ../examples/composite_dependency.py