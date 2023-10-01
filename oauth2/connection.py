from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Tuple, List

import enum
import attrs

from oauth2.integration import PartialIntegration

if TYPE_CHECKING:
    from oauth2.types import ApplicationRoleConnection as ApplicationRoleConnectionResponse, LocalizationDict, ApplicationRoleConnectionMetadata as ApplicationRoleConnectionMetadataResponse, Connection as ConnectionData

__all__: Tuple[str, ...] = (
    "ApplicationRoleConnection",
    "ApplicationRoleConnectionMetadata",
    "MetadataType",
)


class ConnectionType(enum.Enum):
    battlenet = "Battle.net"
    ebay = "eBay"
    epicgames = "Epic Games"
    facebook = "Facebook"
    github = "GitHub"
    instagram = "Instagram"
    leagueoflegends = "League of Legends"
    paypal = "PayPal"
    playstation = "PlayStation Network"
    reddit = "Reddit"
    riotgames = "Riot Games"
    spotify = "Spotify"
    skype = "Skype"
    steam = "Steam"
    tiktok = "TikTok"
    twitch = "Twitch"
    twitter = "X"
    xbox = "Xbox"
    youtube = "YouTube"

    @classmethod
    def from_api(cls, type: str) -> ConnectionType:
        return cls._member_map_[type]  # type: ignore


class VisibilityType(enum.IntEnum):
    NONE = 0
    EVERYONE = 1


@attrs.define(repr=True, slots=True)
class Connection:
    id: int
    name: str
    type: ConnectionType
    verified: bool
    friend_sync: bool
    show_activity: bool
    two_way_link: bool
    visibility: VisibilityType
    integrations: Optional[List[PartialIntegration]]
    revoked: Optional[bool] = False

    @classmethod
    def from_data(cls, data: ConnectionData) -> Connection:
        if integrations_data := data.get("integrations"):
            integrations = [PartialIntegration.from_data(i) for i in integrations_data]
        else:
            integrations = None

        return cls(
            id=data["id"],  # type: ignore
            name=data["name"],
            type=ConnectionType.from_api(data["type"]),
            verified=data["verified"],
            friend_sync=data["friend_sync"],
            show_activity=data["show_activity"],
            two_way_link=data["two_way_link"],
            visibility=VisibilityType(data["visibility"]),
            integrations=integrations,
            revoked=data.get("revoked"),
        )


class MetadataType(enum.IntEnum):
    INTEGER_LESS_THAN_OR_EQUAL = 1
    INTEGER_GREATER_THAN_OR_EQUAL = 2
    INTEGER_EQUAL = 3
    INTEGER_NOT_EQUAL = 4
    DATETIME_LESS_THAN_OR_EQUAL = 5
    DATETIME_GREATER_THAN_OR_EQUAL = 6
    BOOLEAN_EQUAL = 7
    BOOLEAN_NOT_EQUAL = 8


@attrs.define(repr=True, slots=True)
class ApplicationRoleConnectionMetadata:
    type: MetadataType
    key: str
    name: str
    description: str
    name_localizations: Optional[LocalizationDict] = None
    description_localizations: Optional[LocalizationDict] = None

    @classmethod
    def from_data(cls, data: ApplicationRoleConnectionMetadataResponse) -> ApplicationRoleConnectionMetadata:
        return cls(
            type=MetadataType(data["type"]),
            key=data["key"],
            name=data["name"],
            description=data["description"],
            name_localizations=data.get("name_localizations"),
            description_localizations=data.get("description_localizations"),
        )

    def to_dict(self) -> ApplicationRoleConnectionMetadataResponse:
        data: ApplicationRoleConnectionMetadataResponse = {
            "type": self.type.value,
            "key": self.key,
            "name": self.name,
            "description": self.description,
        }

        if self.name_localizations:
            data["name_localizations"] = self.name_localizations
        if self.description_localizations:
            data["description_localizations"] = self.description_localizations

        return data


@attrs.define(repr=True, slots=True)
class ApplicationRoleConnection:
    metadata: ApplicationRoleConnectionMetadata
    platform_name: Optional[str] = None
    platform_username: Optional[str] = None

    @classmethod
    def from_data(cls, data: ApplicationRoleConnectionResponse) -> ApplicationRoleConnection:
        return cls(
            metadata=ApplicationRoleConnectionMetadata.from_data(data["metadata"]),
            platform_name=data["platform_name"],
            platform_username=data["platform_username"],
        )
