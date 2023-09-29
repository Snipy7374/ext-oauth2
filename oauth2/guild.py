from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

import attrs

from oauth2.asset import Asset

if TYPE_CHECKING:
    from oauth2._http import HTTPClient
    from oauth2.types import Emoji, GuildFeature, PartialGuild as PartialGuildPayload


@attrs.define()
class _BaseGuild:
    _http: HTTPClient
    id: int
    name: str
    features: List[GuildFeature]
    _icon: Optional[str]

    @property
    def icon(self) -> Optional[Asset]:
        if self._icon:
            return Asset._from_guild_icon(self._http, self.id, self._icon)

    def __eq__(self, __other: object) -> bool:
        return issubclass(__other.__class__, self.__class__) and self.id == __other.id  # type: ignore


@attrs.define(slots=True, repr=True)
class PartialGuild(_BaseGuild):
    owner: bool
    permissions: int
    approximate_member_count: Optional[int]
    approximate_presence_count: Optional[int]

    @classmethod
    def from_payload(
        cls, payload: PartialGuildPayload, http: HTTPClient
    ) -> PartialGuild:
        return cls(
            _http=http,
            id=payload["id"],  # type: ignore
            name=payload["name"],
            features=payload["features"],
            _icon=payload["icon"],
            owner=payload["owner"],
            permissions=payload["permissions"],
            approximate_member_count=payload.get("approximate_member_count"),
            approximate_presence_count=payload.get("approximate_presence_count"),
        )


@attrs.define(slots=True, repr=True)
class Guild(_BaseGuild):
    mfa_level: int
    emojis: List[str]
    roles: List[Emoji]
    afk_timeout: int
    region: str  # should be deprecated
    default_message_notifications: int
    explicit_content_filter: int
    widget_enabled: bool
    verification_level: int
    owner_id: int
    max_members: int
    premium_subscription_count: int
    premium_tier: int
    preferred_locale: str
    system_channel_flags: int
    max_video_channel_users: int
    application_id: Optional[int] = None
    system_channel_id: Optional[int] = None
    widget_channel_id: Optional[int] = None
    splash: Optional[str] = None  # splash invite?
    afk_channel_id: Optional[int] = None
    description: Optional[str] = None
    public_updates_channel_id: Optional[int] = None
    safety_alerts_channel_id: Optional[int] = None
    rules_channel_id: Optional[int] = None
    vanity_url_code: Optional[str] = None
    banner: Optional[str] = None  # implement an asset or something?
    max_presences: Optional[int] = None
    discovery_splash: Optional[int] = None
