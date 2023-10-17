from __future__ import annotations
from typing import TypedDict, Tuple, Literal, List, Optional
from typing_extensions import NotRequired

from . import Snowflake, PartialIntegration, LocalizationDict

__all__: Tuple[str, ...] = ("Connection", "ApplicationRoleConnection", "ApplicationRoleConnectionMetadata",)


ConnectionType = Literal[
    "battlenet",
    "ebay",
    "epicgames",
    "facebook",
    "github",
    "instagram",
    "leagueoflegends",
    "paypal",
    "playstation",
    "reddit",
    "riotgames",
    "spotify",
    "skype",
    "steam",
    "tiktok",
    "twitch",
    "twitter",
    "xbox",
    "youtube"
]
Visibility = Literal[0, 1]
ApplicationRoleConnectionMetadataType = Literal[1, 2, 3, 4, 5, 6, 7, 8]


class Connection(TypedDict):
    id: Snowflake
    name: str
    type: ConnectionType
    revoked: NotRequired[bool]
    integrations: NotRequired[List[PartialIntegration]]
    verified: bool
    friend_sync: bool
    show_activity: bool
    two_way_link: bool
    visibility: Visibility


class ApplicationRoleConnectionMetadata(TypedDict):
    type: ApplicationRoleConnectionMetadataType
    key: str
    name: str
    name_localizations: NotRequired[LocalizationDict]
    description: str
    description_localizations: NotRequired[LocalizationDict]


class ApplicationRoleConnection(TypedDict):
    platform_name: Optional[str]
    platform_username: Optional[str]
    metadata: ApplicationRoleConnectionMetadata
