from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING

import attrs
import enum

if TYPE_CHECKING:
    from oauth2.types import Team as TeamPayload, TeamMember as TeamMemberPayload


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
    def from_payload(cls, payload: TeamMemberPayload, team: Team) -> TeamMember:
        return cls(
            name=payload["user"]["username"],
            id=payload["user"]["id"],  # type: ignore
            permissions=payload["permissions"],
            membership_state=payload["membership_state"],
            team=team
        )


@attrs.define(slots=True, repr=True)
class Team:
    id: int
    name: str
    members: List[TeamMember]
    _icon: Optional[str] = None
    owner_id: Optional[int] = None

    @classmethod
    def from_payload(cls, payload: TeamPayload) -> Team:
        team = cls(
            id=payload["id"],  # type: ignore
            name=payload["name"],
            members=[],
            _icon=payload.get("icon"),
            owner_id=payload.get("owner_user_id")  # type: ignore
        )
        team.members = [TeamMember.from_payload(i, team) for i in payload["members"]]
        return team
