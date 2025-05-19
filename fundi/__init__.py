import typing as _typing

from .scan import scan
from . import exceptions
from .from_ import from_
from .resolve import resolve
from .inject import inject, ainject
from .util import tree, order, injection_trace
from .types import CallableInfo, TypeResolver, InjectionTrace, R, Parameter
from .configurable import configurable_dependency, MutableConfigurationWarning


FromType: _typing.TypeAlias = _typing.Annotated[R, TypeResolver]
"""Tell resolver to resolve parameter's value by its type, not name"""

__all__ = [
    "scan",
    "tree",
    "order",
    "from_",
    "inject",
    "resolve",
    "ainject",
    "Parameter",
    "exceptions",
    "CallableInfo",
    "TypeResolver",
    "InjectionTrace",
    "injection_trace",
    "configurable_dependency",
    "MutableConfigurationWarning",
]
