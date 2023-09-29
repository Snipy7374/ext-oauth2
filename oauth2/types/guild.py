from __future__ import annotations
from typing import TypedDict, List, Literal, Optional, Tuple, Any
from typing_extensions import NotRequired

from . import Snowflake
from oauth2.types import Emoji, Role, GuildSticker

__all__: Tuple[str, ...] = ("PartialGuild", "GuildFeature", "Guild")


GuildFeature = Literal[
    "ANIMATED_BANNER",
    "ANIMATED_ICON",
    "AUTO_MODERATION",
    "BANNER",
    "COMMUNITY",
    "CREATOR_MONETIZABLE",  # not yet documented/finalised
    "CREATOR_MONETIZABLE_PROVISIONAL",
    "CREATOR_STORE_PAGE",
    "DEVELOPER_SUPPORT_SERVER",
    "DISCOVERABLE",
    "ENABLED_DISCOVERABLE_BEFORE",
    "FEATURABLE",
    "GUILD_HOME_TEST",  # not yet documented/finalised
    "HAS_DIRECTORY_ENTRY",
    "HUB",
    "INVITE_SPLASH",
    "INVITES_DISABLED",
    "LINKED_TO_HUB",
    "MEMBER_PROFILES",  # not sure what this does, if anything
    "MEMBER_VERIFICATION_GATE_ENABLED",
    "MORE_EMOJI",
    "MORE_STICKERS",
    "NEWS",
    "NEW_THREAD_PERMISSIONS",  # deprecated
    "PARTNERED",
    "PREVIEW_ENABLED",
    "PRIVATE_THREADS",  # deprecated
    "RAID_ALERTS_DISABLED",
    "RELAY_ENABLED",
    "ROLE_ICONS",
    "ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE",
    "ROLE_SUBSCRIPTIONS_ENABLED",
    "SEVEN_DAY_THREAD_ARCHIVE",  # deprecated
    "TEXT_IN_VOICE_ENABLED",  # deprecated
    "THREADS_ENABLED",  # deprecated
    "THREE_DAY_THREAD_ARCHIVE",  # deprecated
    "TICKETED_EVENTS_ENABLED",  # deprecated
    "VANITY_URL",
    "VERIFIED",
    "VIP_REGIONS",
    "WELCOME_SCREEN_ENABLED",
]
MFALevel = Literal[0, 1]
DefaultMessageNotificationLevel = Literal[0, 1]
ExplicitContentFilterLevel = Literal[0, 1, 2]
VerificationLevel = Literal[0, 1, 2, 3, 4]
NSFWLevel = Literal[0, 1, 2, 3]
PremiumTier = Literal[0, 1, 2, 3]


class _BaseGuild(TypedDict):
    id: Snowflake
    name: str
    icon: Optional[str]
    features: List[GuildFeature]


class PartialGuild(_BaseGuild):
    owner: bool
    permissions: int
    approximate_member_count: NotRequired[int]
    approximate_presence_count: NotRequired[int]


class Guild(_BaseGuild):
    mfa_level: MFALevel
    emojis: List[Emoji]
    application_id: Optional[Snowflake]
    roles: List[Role]
    afk_timeout: int
    afk_channel_id: Optional[Snowflake]
    system_channel_id: Optional[Snowflake]
    widget_channel_id: Optional[Snowflake]
    region: NotRequired[str]
    default_message_notifications: DefaultMessageNotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    splash: Optional[str]
    widget_enabled: NotRequired[bool]
    verification_level: VerificationLevel
    owner_id: Snowflake
    description: Optional[str]
    public_updates_channel_id: Optional[Snowflake]
    safety_alerts_channel_id: Optional[Snowflake]
    rules_channel_id: Optional[Snowflake]
    max_members: NotRequired[int]
    vanity_url_code: Optional[str]
    premium_subscription_count: NotRequired[int]
    premium_tier: int
    preferred_locale: str
    system_channel_flags: int
    banner: Optional[str]
    max_presences: NotRequired[Optional[int]]
    discovery_splash: Optional[str]
    max_video_channel_users: NotRequired[int]
    stickers: List[GuildSticker]
    max_stage_video_channel_users: NotRequired[int]
    premium_progress_bar_enabled: bool
    nsfw: bool
    nsfw_level: NSFWLevel

    # new undocumented attributes
    # if you know what types they're returning open a PR or reach
    # me out pls!
    latest_onboarding_question_id: Optional[Snowflake] # ? taking a guess
    inventory_settings: Optional[Any] # ?
    incidents_data: Optional[Any] # ?
    hub_type: Optional[Any] # ?
    home_header: Optional[Any] # ?
    embed_enabled: NotRequired[bool] # ? taking a guess
    embed_channel_id: NotRequired[Optional[Snowflake]] # ? taking a guess
