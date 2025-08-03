import typing

from fastapi import params
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import add_param_to_fields, analyze_param

from fundi.types import CallableInfo
from .constants import ALIAS_ALLOWED_CLASSES


def get_scope_dependant(
    ci: CallableInfo[typing.Any], path_param_names: set[str], path: str
) -> Dependant:
    dependant = Dependant(path=path)

    for param in ci.parameters:
        if param.from_ is not None:
            sub = get_scope_dependant(param.from_, path_param_names, path)
            dependant.path_params.extend(sub.path_params)
            dependant.query_params.extend(sub.query_params)
            dependant.header_params.extend(sub.header_params)
            dependant.cookie_params.extend(sub.cookie_params)
            dependant.body_params.extend(sub.body_params)
            continue

        details = analyze_param(
            param_name=param.name,
            annotation=param.annotation,
            value=param.default,
            is_path_param=param.name in path_param_names,
        )

        if details.type_annotation in ALIAS_ALLOWED_CLASSES:
            continue

        assert details.field is not None
        if isinstance(details.field.field_info, params.Body):
            dependant.body_params.append(details.field)
        else:
            add_param_to_fields(field=details.field, dependant=dependant)

    return dependant
