from __future__ import annotations
from typing import TypedDict, Optional, Literal, List, Dict, Tuple

from . import Snowflake
from . import PartialDMUser

__all__: Tuple[str, ...] = (
    "DMChannel",
    "GroupDMChannel",
)


Nick = Dict[Snowflake, str]


class _BaseChannel(TypedDict):
    id: Snowflake


class DMChannel(_BaseChannel):
    ...


class GroupDMChannel(_BaseChannel):
    name: str
    icon: Optional[str]
    type: Literal[3]
    last_message_id: Optional[Snowflake]
    flags: int
    recipients: List[PartialDMUser]
    nicks: List[Nick]
    owner_id: Snowflake
    managed: bool
    application_id: Snowflake
