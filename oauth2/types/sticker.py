from __future__ import annotations

from typing import Literal, Optional, Tuple, TypedDict

from typing_extensions import NotRequired

from . import Snowflake
from .user import User

__all__: Tuple[str, ...] = ("GuildSticker",)

StickerFormatType = Literal[1, 2, 3, 4]


class StickerItem(TypedDict):
    id: Snowflake
    name: str
    format_type: StickerFormatType


class BaseSticker(TypedDict):
    id: Snowflake
    name: str
    description: Optional[str]
    tags: str
    format_type: StickerFormatType


class GuildSticker(BaseSticker):
    type: Literal[2]
    available: NotRequired[bool]
    guild_id: Snowflake
    user: NotRequired[User]
