import typing
from collections.abc import Sequence

from fastapi.security.oauth2 import SecurityScopes

from fundi.scan import scan
from .metadata import get_metadata
from fundi.types import CallableInfo
from .constants import METADATA_SECURITY_SCOPES


def secured(
    dependency: typing.Callable[..., typing.Any], scopes: Sequence[str], caching: bool = True
) -> CallableInfo[typing.Any]:
    """
    Use callable dependency for parameter of function

    :param dependency: function dependency
    :param caching: Whether to use cached result of this callable or not
    :return: callable information
    """

    info = scan(dependency, caching=caching)
    metadata = get_metadata(info)
    metadata.update({METADATA_SECURITY_SCOPES: SecurityScopes(list(scopes))})
    return info
