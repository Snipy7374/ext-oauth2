from __future__ import annotations

import logging
import asyncio
import sys
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Tuple
from urllib.parse import quote as _uriquote

import aiohttp

from oauth2 import __version__

if TYPE_CHECKING:
    from oauth2.types import (
        AccessExchangeTokenPayload,
        AccessTokenResponse,
        ClientCredentialsPayload,
        ClientCredentialsResponse,
        RefreshTokenPayload,
        RevokeTokenPayload,
    )

__all__: Tuple[str, ...] = ("HTTPClient", "Route")
_log = logging.getLogger(__name__)


class Route:
    BASE: ClassVar[str] = "https://discord.com/api/v10"

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.path: str = path
        self.method: str = method
        url = self.BASE + self.path
        if parameters:
            url = url.format_map(
                {
                    k: _uriquote(v) if isinstance(v, str) else v
                    for k, v in parameters.items()
                }
            )
        self.url: str = url


class HTTPClient:
    def __init__(
        self,
        connector: Optional[aiohttp.BaseConnector],
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        self._connector = connector
        self.loop = loop
        self.__session = None

        self.user_agent = f"DiscordApp (https://github.com/Snipy7374/disnake-ext-oauth2 {__version__}) Python/{(py_ver:=sys.version_info)[0]}.{py_ver[1]} aiohttp/{aiohttp.__version__}"

    async def create_session(self) -> None:
        self.__session = aiohttp.ClientSession(connector=self._connector)
        _log.debug("Session object created")

    async def request(self, route: Route, **kwargs: Any) -> Any:
        method = route.method
        url = route.url

        if self.__session is None:
            await self.create_session()

        if headers := kwargs.get("headers"):  # type: ignore
            headers["User-Agent"] = self.user_agent
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            headers: Dict[str, str] = {
                "User-Agent": self.user_agent,
                "Content-Type": "application/x-www-form-urlencoded",
            }

        auth = None
        if auth := kwargs.get("auth"):
            auth = aiohttp.BasicAuth(auth["client_id"], auth["client_secret"])
            _log.debug("Authenticating a request using client credentials as Login and Password")

        payload: Dict[str, str] = kwargs.get("payload") or {}

        async with self.__session.request(method, url, data=payload, headers=headers, auth=auth) as response:  # type: ignore
            response.raise_for_status()
            return await response.json()

    async def _exchange_token(
        self, payload: AccessExchangeTokenPayload
    ) -> AccessTokenResponse:
        return await self.request(
            Route("POST", "/oauth2/token"),
            payload=payload,
        )

    async def _refresh_token(self, payload: RefreshTokenPayload) -> AccessTokenResponse:
        return await self.request(
            Route("POST", "/oauth2/token"),
            payload=payload,
        )

    async def _revoke_token(self, payload: RevokeTokenPayload) -> None:
        return await self.request(
            Route("POST", "/oauth2/token/revoke"),
            payload=payload,
        )

    async def _get_client_credentials_token(
        self, payload: ClientCredentialsPayload, **kwargs: Any
    ) -> ClientCredentialsResponse:
        return await self.request(
            Route("POST", "/oauth2/token"), payload=payload, **kwargs
        )
