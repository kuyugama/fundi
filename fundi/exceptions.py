import typing

from fundi.util import callable_str
from fundi.types import CallableInfo


class ScopeValueNotFoundError(ValueError):
    def __init__(self, parameter: str, info: CallableInfo[typing.Any]):
        super().__init__(
            f'Cannot resolve "{parameter}" for {callable_str(info.call)} - Scope does not contain required value'
        )
        self.parameter: str = parameter
        self.info: CallableInfo[typing.Any] = info
