import typing

from fastapi import params
from fastapi._compat import ModelField
from fastapi.security.base import SecurityBase
from fastapi.security.oauth2 import SecurityScopes
from fastapi.dependencies.models import Dependant, SecurityRequirement
from fastapi.dependencies.utils import add_param_to_fields, analyze_param

from fundi.types import CallableInfo

from .metadata import get_metadata
from .constants import ALIAS_ALLOWED_CLASSES, METADATA_SECURITY_SCOPES

MF = typing.TypeVar("MF", bound=ModelField)


def merge(into: list[MF], from_: list[MF]):
    names = {field.name for field in into}

    for field in from_:
        if field.name not in names:
            into.append(field)


def update_dependant(source: Dependant, target: Dependant):
    merge(target.path_params, source.path_params)
    merge(target.query_params, source.query_params)
    merge(target.header_params, source.header_params)
    merge(target.cookie_params, source.cookie_params)
    merge(target.body_params, source.body_params)

    target.security_requirements.extend(source.security_requirements)
    target.dependencies.extend(source.dependencies)
    if source.security_scopes:
        if target.security_scopes is None:
            target.security_scopes = []

        target.security_scopes.extend(source.security_scopes)


def get_scope_dependant(
    ci: CallableInfo[typing.Any],
    path_param_names: set[str],
    path: str,
    security_scopes: list[str] | None = None,
) -> Dependant:
    if security_scopes is None:
        security_scopes = []

    dependant = Dependant(path=path)
    get_metadata(ci).update(__dependant__=dependant)

    flat_dependant = Dependant(path=path, security_scopes=security_scopes)

    for param in ci.parameters:
        if param.from_ is not None:
            subci = param.from_

            sub = get_scope_dependant(subci, path_param_names, path, security_scopes)
            update_dependant(sub, flat_dependant)

            # This is required to pass security_scopes to dependency.
            # Here parameter name and security scopes itself are set.
            metadata = get_metadata(subci)

            param_scopes: SecurityScopes | None = metadata.get(METADATA_SECURITY_SCOPES, None)

            if param_scopes:
                security_scopes.extend(param_scopes.scopes)

            if isinstance(subci.call, SecurityBase):
                flat_dependant.security_requirements.append(
                    SecurityRequirement(
                        subci.call, security_scopes if param_scopes is None else param_scopes.scopes
                    )
                )

            continue

        details = analyze_param(
            param_name=param.name,
            annotation=param.annotation,
            value=param.default,
            is_path_param=param.name in path_param_names,
        )

        if details.type_annotation is SecurityScopes:
            dependant.security_scopes_param_name = param.name
            continue

        if details.type_annotation in ALIAS_ALLOWED_CLASSES:
            continue

        assert details.field is not None
        if isinstance(details.field.field_info, params.Body):
            dependant.body_params.append(details.field)
        else:
            add_param_to_fields(field=details.field, dependant=dependant)

    update_dependant(dependant, flat_dependant)

    return flat_dependant
