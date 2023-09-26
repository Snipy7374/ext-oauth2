from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

import attrs

if TYPE_CHECKING:
    from oauth2.types import EmojiData


@attrs.define(slots=True, repr=True)
class Guild:
    mfa_level: int
    emojis: List[str]
    name: str
    roles: List[EmojiData]
    afk_timeout: int
    region: str  # should be deprecated
    default_message_notifications: int
    explicit_content_filter: int
    widget_enabled: bool
    verification_level: int
    owner_id: int
    id: int
    max_members: int
    premium_subscription_count: int
    premium_tier: int
    preferred_locale: str
    system_channel_flags: int
    max_video_channel_users: int
    icon: Optional[str] = None  # implement an asset or something?
    application_id: Optional[int] = None
    system_channel_id: Optional[int] = None
    widget_channel_id: Optional[int] = None
    splash: Optional[str] = None # splash invite?
    features: Optional[List[str]] = None
    afk_channel_id: Optional[int] = None
    description: Optional[str] = None
    public_updates_channel_id: Optional[int] = None
    safety_alerts_channel_id: Optional[int] = None
    rules_channel_id: Optional[int] = None
    vanity_url_code: Optional[str] = None
    banner: Optional[str] = None # implement an asset or something?
    max_presences: Optional[int] = None
    discovery_splash: Optional[int] = None
