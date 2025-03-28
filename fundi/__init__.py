import typing

from .scan import scan
from .resolve import resolve
from .util import tree, order
from .types import CallableInfo
from .inject import inject, ainject


def from_(call: typing.Callable[..., typing.Any]) -> CallableInfo:
    """
    Use callable as dependency for parameter of function(alias for fundi.scan.scan)
    :param call: callable to be used as dependency
    :return: callable information
    """
    return scan(call)
