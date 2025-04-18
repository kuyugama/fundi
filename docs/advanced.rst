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
By default, FunDI automatically caches all dependency results,
so you can use dependencies whether you need not bothering
about data duplicates

  To disable this behavior - use :code:`caching` parameter when defining dependant's dependency

.. literalinclude:: ../examples/caching.py

Scope
=====
Library provides injection scope, that allows to inject values to dependencies parameters by name

.. literalinclude:: ../examples/scope.py


Scope by type
=============
Dependency parameters can resolve their values from scope by type using `from_`

.. literalinclude:: ../examples/scope_by_type.py
