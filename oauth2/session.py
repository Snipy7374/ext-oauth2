from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional, Union

import attrs

from oauth2.appinfo import AuthorizationInfo
from oauth2.user import User
from oauth2.utils import to_datetime, to_int

if TYPE_CHECKING:
    from oauth2.client import Client
    from oauth2.types import AccessTokenResponse, ClientCredentialsResponse


@attrs.define(slots=True, repr=True)
class OAuth2Session:
    access_token: str
    token_type: str
    expires_in: datetime.datetime = attrs.field(converter=to_datetime)
    scope: str
    _client: Client
    state_security_key: Optional[str] = None
    refresh_token: Optional[str] = None
    guild_id: Optional[int] = attrs.field(default=None, converter=to_int)
    permissions: Optional[int] = attrs.field(default=None, converter=to_int)

    def _update(self, data: AccessTokenResponse) -> None:
        for k, v in data.items():
            self.__setattr__(k, v)

    @classmethod
    def from_data(
        cls,
        data: Union[AccessTokenResponse, ClientCredentialsResponse],
        state: Optional[str],
        client: Client,
    ) -> OAuth2Session:
        return cls(
            data["access_token"],
            data["token_type"],
            data["expires_in"],
            data["scope"],
            client,
            state,
            data.get("refresh_token"),
            data.get("guild_id"),  # type: ignore
            data.get("permissions"),  # type: ignore
        )

    @property
    def client(self) -> Client:
        return self._client

    @property
    def is_expired(self) -> bool:
        return (
            datetime.datetime.now(datetime.timezone.utc)
        ).timestamp() >= self.expires_in.timestamp()

    async def refresh(self) -> None:
        if not self.refresh_token:
            raise ValueError(
                f"Couldn't refresh the token because {self.refresh_token!r}"
            )
        data = await self._client.http._refresh_token(refresh_token=self.refresh_token)
        self._update(data)

    async def revoke(self) -> None:
        await self._client.http._revoke_token(
            token=self.access_token, token_type=self.token_type
        )

    async def fetch_current_authorization_info(self) -> AuthorizationInfo:
        data = await self._client.http._get_current_auth_info(self.access_token)
        return AuthorizationInfo.from_data(data, self._client.http)

    async def fetch_current_user(self) -> User:
        data = await self._client.http._get_current_user(self.access_token)
        return User.from_data(data, self._client.http, self)
