import typing

from fundi.scan import scan
from fundi.types import CallableInfo, TypeResolver


def from_(dependency: type | typing.Callable[..., typing.Any]) -> TypeResolver | CallableInfo:
    """
    Use callable or type as dependency for parameter of function

    if dependency parameter is callable the ``fundi.scan.scan`` is used

    if dependency parameter is type the ``fundi.types.TypeResolver`` is returned

    :param dependency: function dependency
    :return: callable information
    """
    if isinstance(dependency, type):
        return TypeResolver(dependency)

    return scan(dependency)
