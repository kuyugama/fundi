**************
Advanced usage
**************

Lifespan
========
Library allows to create "lifespan" dependencies that can clean-up some
resources after data they returned was used

.. literalinclude:: ../examples/lifespan.py

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
