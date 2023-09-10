from __future__ import annotations

import logging
import asyncio
from typing import Optional, Tuple, Union

import aiohttp

from oauth2._http import HTTPClient
from oauth2.token import AccessToken


__all__: Tuple[str, ...] = ("Client",)
_log = logging.getLogger(__name__)


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
        data = await self.http._exchange_token(id=self.id, secret=self._secret, code=code, redirect_uri=self.redirect_uri)
        return AccessToken.from_data(data)

    async def refresh_token(self, refresh_token: str) -> AccessToken:
        data = await self.http._refresh_token(id=self.id, secret=self._secret, refresh_token=refresh_token)
        return AccessToken.from_data(data)

    async def revoke_token(
        self, token: Union[AccessToken, str], *, token_type: Optional[str] = None
    ) -> None:
        if isinstance(token, AccessToken) and token_type:
            raise ValueError("Can't provide 'token_type' in conjunction with 'token'")

        if isinstance(token, str) and not token_type:
            raise ValueError(
                "The 'token_type' argument is required if passing a string token"
            )

        await self.http._revoke_token(
            id=self.id,
            secret=self._secret,
            token=(
                token.access_token if isinstance(token, AccessToken) else token
            ),
            token_type=(
                token.token_type if isinstance(token, AccessToken) else token_type  # type: ignore
            )
        )

    async def get_client_credentials_token(self) -> AccessToken:
        data = await self.http._get_client_credentials_token(auth={"client_id": str(self.id), "client_secret": self._secret})
        return AccessToken.from_data(data)
