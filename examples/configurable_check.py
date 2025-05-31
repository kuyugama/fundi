from fundi import is_configured, configurable_dependency


@configurable_dependency
def auth(optional: bool = False):
    return lambda: optional


assert is_configured(auth())
