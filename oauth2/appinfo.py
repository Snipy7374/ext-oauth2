from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, List, Optional

import attrs

from oauth2.asset import Asset
from oauth2.scopes import OAuthScopes
from oauth2.team import Team
from oauth2.utils import _to_install_params, _to_oauth2_scopes

if TYPE_CHECKING:
    from oauth2._http import HTTPClient
    from oauth2.types import (
        AppInfo as AppInfoData,
        AuthInfo as AuthInfoData,
        PartialAppInfo as PartialAppInfoData,
    )


@attrs.define(slots=True, repr=True)
class InstallParams:
    scopes: OAuthScopes
    permissions: int


@attrs.define(slots=True, repr=True)
class AppInfo:
    _http: HTTPClient
    id: int
    name: str
    description: str
    bot_public: bool
    bot_require_code_grant: bool
    owner: ...  # User
    verify_key: str
    rpc_origins: Optional[List[str]] = None
    _cover_image: Optional[str] = None
    terms_of_service_url: Optional[str] = None
    privacy_policy_url: Optional[str] = None
    flags: Optional[int] = None
    team: Optional[Team] = None
    guild_id: Optional[int] = None
    primary_sku_id: Optional[int] = None
    slug: Optional[str] = None
    tags: Optional[List[str]] = None
    install_params: Optional[InstallParams] = attrs.field(
        default=None, converter=_to_install_params
    )
    custom_install_url: Optional[str] = None
    role_connections_verification_url: Optional[str] = None
    _icon: Optional[str] = None

    @classmethod
    def from_data(cls, data: AppInfoData, http: HTTPClient) -> AppInfo:
        team_data = data.get("team")
        owner_data = data.get("owner")
        install_params_data = data.get("install_params")

        return cls(
            _http=http,
            id=data["id"],  # type: ignore
            name=data["name"],
            description=data["description"],
            terms_of_service_url=data.get("terms_of_service_url"),
            privacy_policy_url=data.get("privacy_policy_url"),
            verify_key=data["verify_key"],
            rpc_origins=data.get("rpc_origins"),
            bot_public=data["bot_public"],
            bot_require_code_grant=data["bot_require_code_grant"],
            owner=owner_data,
            team=(Team.from_data(team_data) if team_data else None),
            guild_id=data.get("guild_id"),  # type: ignore
            primary_sku_id=data.get("primary_sku_id"),  # type: ignore
            slug=data.get("slug"),
            tags=data.get("tags"),
            install_params=install_params_data,
            custom_install_url=data.get("custom_install_url"),
            role_connections_verification_url=data.get(
                "role_connections_verification_url"
            ),
        )

    @property
    def icon(self) -> Optional[Asset]:
        if self._icon:
            return Asset._from_icon(self._http, self.id, self._icon, path="app")

    @property
    def cover_image(self) -> Optional[Asset]:
        if self._cover_image:
            return Asset._from_cover_image(self._http, self.id, self._cover_image)


@attrs.define(slots=True, repr=True, kw_only=True)
class PartialAppInfo:
    id: int
    name: str
    description: str
    verify_key: str
    _http: HTTPClient
    rpc_origins: Optional[List[str]] = None
    _icon: Optional[str] = None
    terms_of_service_url: Optional[str] = None
    privacy_policy_url: Optional[str] = None

    @property
    def icon(self) -> Optional[Asset]:
        if self._icon:
            return Asset._from_icon(self._http, self.id, self._icon, path="app")

    @classmethod
    def from_data(cls, data: PartialAppInfoData, http: HTTPClient) -> PartialAppInfo:
        return cls(
            id=data["id"],  # type: ignore
            name=data["name"],
            description=data["description"],
            verify_key=data["verify_key"],
            rpc_origins=data.get("rpc_origins"),
            icon=data.get("icon"),  # type: ignore
            terms_of_service_url=data.get("terms_of_service_url"),
            privacy_policy_url=data.get("privacy_policy_url"),
            http=http,  # type: ignore
        )


@attrs.define(slots=True, repr=True)
class AuthorizationInfo:
    application: PartialAppInfo
    scopes: OAuthScopes = attrs.field(converter=_to_oauth2_scopes)
    expires: datetime.datetime = attrs.field(converter=datetime.datetime.fromisoformat)
    user: ...

    @classmethod
    def from_data(cls, data: AuthInfoData, http: HTTPClient) -> AuthorizationInfo:
        return cls(
            application=PartialAppInfo.from_data(data["application"], http),
            scopes=data["scopes"],
            expires=data["expires"],
            user=data["user"],
        )
