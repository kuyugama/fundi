import inspect

from fundi import get_configuration, configurable_dependency


@configurable_dependency
def auth(optional: bool = False):
    return lambda: optional


config = get_configuration(auth())

origin = inspect.unwrap(auth)

assert config.configurator.call == origin
assert config.values == {"optional": False}
