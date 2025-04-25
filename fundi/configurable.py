import typing
import warnings
import functools

from fundi.types import R
from fundi.scan import scan
from fundi.util import _callable_str

P = typing.ParamSpec("P")


def configurable_dependency(configurator: typing.Callable[P, R]) -> typing.Callable[P, R]:
    dependencies: dict[tuple[tuple, frozenset], R] = {}
    info = scan(configurator)

    if info.async_:
        raise ValueError("Dependency configurator should not be asynchronous")

    @functools.wraps(configurator)
    def cached_dependency_generator(*args: typing.Any, **kwargs: typing.Any) -> R:
        use_cache = True
        key = (args, frozenset(kwargs.items()))

        try:
            hash(key)
        except TypeError:
            warnings.warn(
                f"Can't cache dependency created via {_callable_str(configurator)}: configured with unhashable arguments",
                UserWarning,
            )
            use_cache = False

        if use_cache and key in dependencies:
            return dependencies[key]

        dependency = configurator(*args, **kwargs)
        setattr(dependency, "__fundi_configuration__", (args, kwargs))

        if use_cache:
            dependencies[key] = dependency

        return dependency

    return cached_dependency_generator
