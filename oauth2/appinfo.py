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
        AppInfo as AppInfoPayload,
        AuthInfo as AuthInfoPayload,
        PartialAppInfo as PartialAppInfoPayload,
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
    def from_payload(cls, payload: AppInfoPayload, http: HTTPClient) -> AppInfo:
        team_payload = payload.get("team")
        owner_payload = payload.get("owner")
        install_params_payload = payload.get("install_params")

        return cls(
            _http=http,
            id=payload["id"],  # type: ignore
            name=payload["name"],
            description=payload["description"],
            terms_of_service_url=payload.get("terms_of_service_url"),
            privacy_policy_url=payload.get("privacy_policy_url"),
            verify_key=payload["verify_key"],
            rpc_origins=payload.get("rpc_origins"),
            bot_public=payload["bot_public"],
            bot_require_code_grant=payload["bot_require_code_grant"],
            owner=owner_payload,
            team=(Team.from_payload(team_payload) if team_payload else None),
            guild_id=payload.get("guild_id"),  # type: ignore
            primary_sku_id=payload.get("primary_sku_id"),  # type: ignore
            slug=payload.get("slug"),
            tags=payload.get("tags"),
            install_params=install_params_payload,
            custom_install_url=payload.get("custom_install_url"),
            role_connections_verification_url=payload.get(
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
    def from_payload(
        cls, payload: PartialAppInfoPayload, http: HTTPClient
    ) -> PartialAppInfo:
        return cls(
            id=payload["id"],  # type: ignore
            name=payload["name"],
            description=payload["description"],
            verify_key=payload["verify_key"],
            rpc_origins=payload.get("rpc_origins"),
            icon=payload.get("icon"),  # type: ignore
            terms_of_service_url=payload.get("terms_of_service_url"),
            privacy_policy_url=payload.get("privacy_policy_url"),
            http=http,  # type: ignore
        )


@attrs.define(slots=True, repr=True)
class AuthorizationInfo:
    application: PartialAppInfo
    scopes: OAuthScopes = attrs.field(converter=_to_oauth2_scopes)
    expires: datetime.datetime = attrs.field(converter=datetime.datetime.fromisoformat)
    user: ...

    @classmethod
    def from_payload(
        cls, payload: AuthInfoPayload, http: HTTPClient
    ) -> AuthorizationInfo:
        return cls(
            application=PartialAppInfo.from_payload(payload["application"], http),
            scopes=payload["scopes"],
            expires=payload["expires"],
            user=payload["user"],
        )
