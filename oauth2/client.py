from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Optional, Tuple, Union

import aiohttp

from oauth2._http import HTTPClient
from oauth2.token import AccessToken

if TYPE_CHECKING:
    from oauth2.types.payloads import (
        AccessExchangeTokenPayload,
        ClientCredentialsPayload,
        RefreshTokenPayload,
        RevokeTokenPayload,
    )

__all__: Tuple[str, ...] = ("Client",)


class Client:
    def __init__(
        self,
        client_id: int,
        *,
        client_secret: str,
        redirect_uri: str,
        connector: Optional[aiohttp.BaseConnector] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self.id = client_id
        self._secret = client_secret
        self.redirect_uri = redirect_uri
        # should raise a deprecation warning
        self.loop = loop or asyncio.get_event_loop()
        self.http = HTTPClient(connector, self.loop)

    async def exchange_code(self, code: str) -> AccessToken:
        payload: AccessExchangeTokenPayload = {
            "client_id": self.id,
            "client_secret": self._secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }

        return AccessToken.from_data(await self.http._exchange_token(payload))

    async def refresh_token(self, refresh_token: str) -> AccessToken:
        payload: RefreshTokenPayload = {
            "client_id": self.id,
            "client_secret": self._secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        return AccessToken.from_data(await self.http._refresh_token(payload))

    async def revoke_token(
        self, token: Union[AccessToken, str], *, token_type: Optional[str] = None
    ) -> None:
        if isinstance(token, AccessToken) and token_type:
            raise ValueError("Can't provide 'token_type' in conjunction with 'token'")

        if isinstance(token, str) and not token_type:
            raise ValueError(
                "The 'token_type' argument is required if passing a string token"
            )

        payload: RevokeTokenPayload = {
            "client_id": self.id,
            "client_secret": self._secret,
            "token": (token.access_token if isinstance(token, AccessToken) else token),
            "token_type": (
                token.token_type
                if isinstance(token, AccessToken)
                else token_type  # type: ignore
            ),
        }

        await self.http._revoke_token(payload)

    async def get_client_credentials_token(self) -> AccessToken:
        payload: ClientCredentialsPayload = {
            "grant_type": "client_credentials",
            "scope": "identify",
        }

        return AccessToken.from_data(
            await self.http._get_client_credentials_token(
                payload, auth={"client_id": str(self.id), "client_secret": self._secret}
            )
        )
