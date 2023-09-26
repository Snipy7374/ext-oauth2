from __future__ import annotations

import asyncio
import logging
from typing import Optional, Tuple

import aiohttp

from oauth2._http import HTTPClient
from oauth2.appinfo import AppInfo
from oauth2.scopes import OAuthScopes
from oauth2.session import OAuth2Session

__all__: Tuple[str, ...] = ("Client",)
_log = logging.getLogger(__name__)


class Client:
    def __init__(
        self,
        client_id: int,
        *,
        scopes: OAuthScopes,
        client_secret: str,
        redirect_uri: str,
        bot_token: Optional[str] = None,
        connector: Optional[aiohttp.BaseConnector] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self._scopes = scopes

        # should raise a deprecation warning
        self.loop = loop or asyncio.get_event_loop()
        self.http = HTTPClient(
            connector,
            self.loop,
            client_id=client_id,
            client_secret=client_secret,
            bot_token=bot_token,
        )

    async def exchange_code(self, code: str) -> OAuth2Session:
        data = await self.http._exchange_token(
            code=code, redirect_uri=self.redirect_uri
        )
        return OAuth2Session.from_data(data, self)

    async def get_client_credentials_token(self) -> OAuth2Session:
        data = await self.http._get_client_credentials_token()
        return OAuth2Session.from_data(data, self)

    async def get_application_info(self) -> AppInfo:
        data = await self.http._get_app_info()
        return AppInfo.from_payload(data, self.http)
