from typing import Tuple, TypedDict, List

from typing_extensions import NotRequired

from . import ApplicationRoleConnectionMetadata, Guild
from . import Snowflake
from .channel import Nick

__all__: Tuple[str, ...] = (
    "AccessExchangeTokenPayload",
    "AccessTokenResponse",
    "AccessTokenDict",
    "ClientCredentialsPayload",
    "ClientCredentialsResponse",
    "RefreshTokenPayload",
    "RevokeTokenPayload",
    "GetGuildsParams",
    "AppRoleConnectionPayload",
    "AddGuildMemberPayload",
    "CreateGroupDMPayload",
)


class _TokenPayload(TypedDict):
    client_id: int
    client_secret: str
    grant_type: str


class AccessExchangeTokenPayload(_TokenPayload):
    code: str
    redirect_uri: str


class _AccessToken(TypedDict):
    access_token: str
    token_type: str
    scope: str
    expires_in: str


class AccessTokenResponse(_AccessToken):
    refresh_token: str
    guild: NotRequired[Guild]


class ClientCredentialsPayload(TypedDict):
    grant_type: str
    scope: NotRequired[str]


ClientCredentialsResponse = _AccessToken


class AccessTokenDict(_AccessToken):
    refresh_token: str


class RefreshTokenPayload(_TokenPayload):
    refresh_token: str


class RevokeTokenPayload(TypedDict):
    client_id: int
    client_secret: str
    token: str
    token_type: str


class GetGuildsParams(TypedDict, total=False):
    before: int
    after: int
    limit: int
    with_counts: bool


class AppRoleConnectionPayload(TypedDict, total=False):
    platform_name: str
    platform_username: str
    metadata: ApplicationRoleConnectionMetadata


class AddGuildMemberPayload(TypedDict):
    access_token: str
    nick: NotRequired[str]
    roles: NotRequired[List[Snowflake]]
    mute: NotRequired[bool]
    deaf: NotRequired[bool]


class CreateGroupDMPayload(TypedDict):
    access_tokens: List[str]
    nicks: List[Nick]
