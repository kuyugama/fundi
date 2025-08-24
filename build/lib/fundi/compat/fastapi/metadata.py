import typing

from fastapi import params
from fastapi.security.oauth2 import SecurityScopes

from fundi.compat.fastapi.constants import METADATA_SCOPE_EXTRA, METADATA_SECURITY_SCOPES
from fundi.types import CallableInfo


def get_metadata(info: CallableInfo[typing.Any]) -> dict[str, typing.Any]:
    metadata: dict[str, typing.Any] | None = getattr(info, "metadata", None)
    if metadata is None:
        metadata = {}
        setattr(info, "metadata", metadata)

    return metadata


def build_metadata(info: CallableInfo[typing.Any]) -> None:
    metadata = get_metadata(info)
    security_scopes: SecurityScopes = metadata.setdefault(
        METADATA_SECURITY_SCOPES, SecurityScopes([])
    )

    for parameter in info.parameters:
        if parameter.from_ is None:
            if parameter.annotation is SecurityScopes:
                metadata.setdefault(METADATA_SCOPE_EXTRA, {}).update(
                    {parameter.name: security_scopes}
                )

            continue

        subinfo = parameter.from_

        param_metadata = get_metadata(subinfo)

        if typing.get_origin(parameter.annotation) is typing.Annotated:
            args = typing.get_args(parameter.annotation)
            presence: tuple[params.Security] | tuple[()] = tuple(
                filter(lambda x: isinstance(x, params.Security), args)
            )

            if presence:
                security = presence[0]
                security_scopes.scopes[::] = list(
                    set(list(security.scopes) + security_scopes.scopes)
                )
                param_metadata.update({METADATA_SECURITY_SCOPES: security_scopes})

        build_metadata(subinfo)
