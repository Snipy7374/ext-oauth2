# thanks disnake

from __future__ import annotations

from typing import List, Optional, Tuple, TypedDict

from typing_extensions import NotRequired

from oauth2.types import Snowflake, Team, User

__all__: Tuple[str, ...] = (
    "AppInfo",
    "PartialAppInfo",
    "InstallParams",
    "AuthInfo",
)


class BaseAppInfo(TypedDict):
    id: Snowflake
    name: str
    icon: Optional[str]
    description: str
    terms_of_service_url: NotRequired[str]
    privacy_policy_url: NotRequired[str]
    verify_key: str
    hook: NotRequired[bool]
    max_participants: NotRequired[int]


class InstallParams(TypedDict):
    scopes: List[str]
    permissions: str


class AppInfo(BaseAppInfo):
    rpc_origins: NotRequired[List[str]]
    bot_public: bool
    bot_require_code_grant: bool
    owner: User
    team: NotRequired[Team]
    guild_id: NotRequired[Snowflake]
    primary_sku_id: NotRequired[Snowflake]
    slug: NotRequired[str]
    tags: NotRequired[List[str]]
    install_params: NotRequired[InstallParams]
    custom_install_url: NotRequired[str]
    role_connections_verification_url: NotRequired[str]


class PartialAppInfo(BaseAppInfo, total=False):
    rpc_origins: List[str]
    cover_image: str
    flags: int


class AuthInfo(TypedDict):
    application: PartialAppInfo
    scopes: List[str]
    expires: str
    user: User
