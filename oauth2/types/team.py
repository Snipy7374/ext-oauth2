# thanks disnake

from __future__ import annotations

from typing import List, Literal, Optional, TypedDict, Tuple

from oauth2.types import Snowflake
from .user import PartialUser

__all__: Tuple[str, ...] = ("Team", "TeamMember",)


TeamMembershipState = Literal[1, 2]


class TeamMember(TypedDict):
    user: PartialUser
    membership_state: TeamMembershipState
    permissions: List[str]
    team_id: Snowflake


class Team(TypedDict):
    id: Snowflake
    name: str
    owner_user_id: Snowflake
    members: List[TeamMember]
    icon: Optional[str]
