import typing
from collections import defaultdict

from pydantic.v1.utils import lenient_issubclass

from fundi.types import CallableInfo
from .constants import ALIAS_ALLOWED_CLASSES


def get_request_related_aliases(ci: CallableInfo[typing.Any]) -> dict[type, set[str]]:
    aliases: defaultdict[type, set[str]] = defaultdict(set)
    for parameter in ci.parameters:
        if parameter.from_ is not None:
            subaliases = get_request_related_aliases(parameter.from_)
            for type_, aliases_ in subaliases.items():
                aliases[type_].update(aliases_)
            continue

        origin = typing.get_origin(parameter.annotation) or parameter.annotation

        for type_ in ALIAS_ALLOWED_CLASSES:
            if lenient_issubclass(origin, type_):
                aliases[type_].add(parameter.name)
    return aliases
