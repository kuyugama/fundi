import typing
import warnings
import functools

from fundi.scan import scan
from fundi.util import callable_str
from fundi.types import R, DependencyConfiguration

P = typing.ParamSpec("P")


class MutableConfigurationWarning(UserWarning):
    pass


def configurable_dependency(configurator: typing.Callable[P, R]) -> typing.Callable[P, R]:
    """
    Create dependency configurator that caches configured dependencies.
    This helps FunDI cache resolver understand that dependency already executed, if it was.

    Note: Calls with mutable arguments will not be stored in cache and warning would be shown

    :param configurator: Original dependency configurator
    :return: cache aware dependency configurator
    """
    dependencies: dict[frozenset[tuple[str, typing.Any]], R] = {}
    info = scan(configurator)

    if info.async_:
        raise ValueError("Dependency configurator should not be asynchronous")

    @functools.wraps(configurator)
    def cached_dependency_generator(*args: typing.Any, **kwargs: typing.Any) -> R:
        use_cache = True
        values = info.build_values(*args, **kwargs)
        key: frozenset[tuple[str, typing.Any]] | None = None

        try:
            key = frozenset(values.items())

            if key in dependencies:
                return dependencies[key]
        except TypeError:
            warnings.warn(
                f"Can't cache dependency created via {callable_str(configurator)}: configured with unhashable arguments",
                MutableConfigurationWarning,
            )
            use_cache = False

        dependency = configurator(*args, **kwargs)
        setattr(
            dependency,
            "__fundi_configuration__",
            DependencyConfiguration(configurator=info, values=values),
        )

        if use_cache and key is not None:
            dependencies[key] = dependency

        return dependency

    return cached_dependency_generator
