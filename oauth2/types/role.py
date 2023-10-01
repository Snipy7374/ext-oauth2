# thanks disnake

from __future__ import annotations

from typing import Optional, Tuple, TypedDict

from typing_extensions import NotRequired

from . import Snowflake

__all__: Tuple[str, ...] = ("Role",)


class Role(TypedDict):
    id: Snowflake
    name: str
    color: int
    hoist: bool
    icon: NotRequired[Optional[str]]
    unicode_emoji: NotRequired[Optional[str]]
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: NotRequired[RoleTags]
    flags: int


class RoleTags(TypedDict, total=False):
    bot_id: Snowflake
    integration_id: Snowflake
    premium_subscriber: None
    guild_connections: None
    subscription_listing_id: Snowflake
    available_for_purchase: None
