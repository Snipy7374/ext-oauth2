from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

import attrs

from oauth2.user import User

if TYPE_CHECKING:
    from oauth2._http import HTTPClient
    from oauth2.types import GroupDMChannel as GroupDMChannelPayload


@attrs.define(slots=True, repr=True)
class GroupDMChannel:
    id: int
    recipients: List[User]
    owner_id: int
    _icon: Optional[str]
    name: Optional[str]
    _http: HTTPClient

    @classmethod
    def from_data(cls, data: GroupDMChannelPayload, http: HTTPClient) -> GroupDMChannel:
        return cls(
            data["id"],
            [User.from_data(user, http) for user in data["recipients"]],
            data["owner_id"],
            data["icon"],
            data["name"],
            http,
        )
