from fundi.util import callable_str
from fundi.types import CallableInfo
from fundi.util import _callable_str


class ScopeValueNotFoundError(ValueError):
    def __init__(self, parameter: str, info: CallableInfo):
        super().__init__(
            f'Cannot resolve "{parameter}" for {callable_str(info.call)} - Scope does not contain required value'
        )
        self.parameter = parameter
        self.info = info
