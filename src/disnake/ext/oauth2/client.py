from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Optional, Tuple

import aiohttp

from ._http import HTTP

if TYPE_CHECKING:
    from .types.payloads import ExchangeTokenPayload

__all__: Tuple[str, ...] = ("Client",)


class Client:
    def __init__(
        self,
        client_id: int,
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
        self.http = HTTP(connector, self.loop)

    async def exchange_code(self, code: str):
        payload: ExchangeTokenPayload = {
            "client_id": self.id,
            "client_secret": self._secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
