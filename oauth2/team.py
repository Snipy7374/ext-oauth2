from __future__ import annotations

import enum
from typing import TYPE_CHECKING, List, Optional

import attrs

if TYPE_CHECKING:
    from oauth2.types import Team as TeamData, TeamMember as TeamMemberData


# this is ugly but whatever
def _to_enum(_v: int) -> TeamMembershipState:
    return TeamMembershipState.invited if _v == 1 else TeamMembershipState.accepted


class TeamMembershipState(enum.IntEnum):
    invited = 1
    accepted = 2


@attrs.define(slots=True, repr=True)
class TeamMember:
    name: str
    id: int
    permissions: List[str]
    membership_state: TeamMembershipState = attrs.field(converter=_to_enum)
    team: Team

    @classmethod
    def from_data(cls, data: TeamMemberData, team: Team) -> TeamMember:
        return cls(
            name=data["user"]["username"],
            id=data["user"]["id"],  # type: ignore
            permissions=data["permissions"],
            membership_state=data["membership_state"],
            team=team,
        )


@attrs.define(slots=True, repr=True)
class Team:
    id: int
    name: str
    members: List[TeamMember]
    _icon: Optional[str] = None
    owner_id: Optional[int] = None

    @classmethod
    def from_data(cls, data: TeamData) -> Team:
        team = cls(
            id=data["id"],  # type: ignore
            name=data["name"],
            members=[],
            _icon=data.get("icon"),
            owner_id=data.get("owner_user_id"),  # type: ignore
        )
        team.members = [TeamMember.from_data(i, team) for i in data["members"]]
        return team
