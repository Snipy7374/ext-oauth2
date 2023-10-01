from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import attrs

if TYPE_CHECKING:
    from oauth2.types import IntegrationType, PartialIntegration as PartialIntegrationData, IntegrationAccount as IntegrationAccountData


@attrs.define(repr=True, slots=True)
class IntegrationAccount:
    id: int
    name: str

    @classmethod
    def from_data(cls, data: IntegrationAccountData) -> IntegrationAccount:
        return cls(
            id=data["id"],  # type: ignore
            name=data["name"]
        )


@attrs.define(repr=True, slots=True)
class PartialIntegration:
    id: int
    name: str
    type: IntegrationType
    account: IntegrationAccount
    application_id: Optional[int]

    @classmethod
    def from_data(cls, data: PartialIntegrationData) -> PartialIntegration:
        return cls(
            id=data["id"],  # type: ignore
            name=data["name"],
            type=data["type"],
            account=IntegrationAccount.from_data(data["account"]),
            application_id=data.get("application_id"),  # type: ignore
        )
