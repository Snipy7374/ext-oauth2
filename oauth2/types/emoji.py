# thanks disnake

from typing import Optional, Tuple, TypedDict

from . import Snowflake, SnowflakeList
from .user import User

__all__: Tuple[str, ...] = ("PartialEmoji", "Emoji")


class PartialEmoji(TypedDict):
    id: Optional[Snowflake]
    name: Optional[str]


class Emoji(PartialEmoji, total=False):
    roles: SnowflakeList
    user: User
    require_colons: bool
    managed: bool
    animated: bool
    available: bool
