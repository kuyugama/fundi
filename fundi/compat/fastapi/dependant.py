import typing

from fastapi import params
from fastapi.security.base import SecurityBase
from fastapi.security.oauth2 import SecurityScopes
from fastapi.dependencies.models import Dependant, SecurityRequirement
from fastapi.dependencies.utils import add_param_to_fields, analyze_param

from fundi.types import CallableInfo

from .metadata import get_metadata
from .constants import ALIAS_ALLOWED_CLASSES, METADATA_SECURITY_SCOPES


def update_dependant(source: Dependant, target: Dependant):
    target.path_params.extend(source.path_params)
    target.query_params.extend(source.query_params)
    target.header_params.extend(source.header_params)
    target.cookie_params.extend(source.cookie_params)
    target.body_params.extend(source.body_params)
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

    dependant = Dependant(path=path, security_scopes=security_scopes)

    for param in ci.parameters:
        if param.from_ is not None:
            subci = param.from_

            sub = get_scope_dependant(subci, path_param_names, path, security_scopes)
            update_dependant(sub, dependant)

            # This is required to pass security_scopes to dependency.
            # Here parameter name and security scopes itself are set.
            metadata = get_metadata(subci)

            param_scopes: SecurityScopes | None = metadata.get(METADATA_SECURITY_SCOPES, None)

            if param_scopes:
                security_scopes.extend(param_scopes.scopes)

            if isinstance(subci.call, SecurityBase):
                dependant.security_requirements.append(
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

    return dependant
