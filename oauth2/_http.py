from __future__ import annotations

import asyncio
import logging
import sys
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Tuple
from urllib.parse import quote as _uriquote

import aiohttp

from oauth2 import __version__

if TYPE_CHECKING:
    from oauth2.types import (
        AccessExchangeTokenPayload,
        AccessTokenResponse,
        AppInfo,
        AuthInfo,
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
        *,
        client_id: int,
        client_secret: str,
        bot_token: Optional[str],
    ) -> None:
        self._connector = connector
        self.loop = loop
        self.__session = None
        self._client_id = client_id
        self.__client_secret = client_secret
        self.__bot_token = bot_token

        self.user_agent = f"DiscordApp (https://github.com/Snipy7374/disnake-ext-oauth2 {__version__}) Python/{(py_ver:=sys.version_info)[0]}.{py_ver[1]} aiohttp/{aiohttp.__version__}"

    async def create_session(self) -> None:
        self.__session = aiohttp.ClientSession(connector=self._connector)
        _log.debug("Session object created")

    async def get_from_cdn(self, url: str) -> bytes:
        if self.__session is None:
            await self.create_session()

        async with self.__session.get(url) as resp:  # type: ignore
            resp.raise_for_status()
            return await resp.read()

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
        if kwargs.get("auth"):
            auth = aiohttp.BasicAuth(str(self._client_id), self.__client_secret)
            _log.debug(
                "Authenticating a request using client credentials as Login and Password"
            )

        payload: Dict[str, str] = kwargs.get("payload") or {}

        async with self.__session.request(method, url, data=payload, headers=headers, auth=auth) as response:  # type: ignore
            response.raise_for_status()
            return await response.json()

    async def _exchange_token(
        self, *, code: str, redirect_uri: str
    ) -> AccessTokenResponse:
        payload: AccessExchangeTokenPayload = {
            "client_id": self._client_id,
            "client_secret": self.__client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        return await self.request(
            Route("POST", "/oauth2/token"),
            payload=payload,
        )

    async def _refresh_token(self, *, refresh_token: str) -> AccessTokenResponse:
        payload: RefreshTokenPayload = {
            "client_id": self._client_id,
            "client_secret": self.__client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        return await self.request(
            Route("POST", "/oauth2/token"),
            payload=payload,
        )

    async def _revoke_token(self, *, token: str, token_type: str) -> None:
        payload: RevokeTokenPayload = {
            "client_id": self._client_id,
            "client_secret": self.__client_secret,
            "token": token,
            "token_type": token_type,
        }

        return await self.request(
            Route("POST", "/oauth2/token/revoke"),
            payload=payload,
        )

    async def _get_client_credentials_token(self) -> ClientCredentialsResponse:
        payload: ClientCredentialsPayload = {
            "grant_type": "client_credentials",
            "scope": "identify",
        }

        return await self.request(
            Route("POST", "/oauth2/token"), payload=payload, auth=True
        )

    async def _get_app_info(self) -> AppInfo:
        return await self.request(
            Route("GET", "/oauth2/applications/@me"),
            headers={"Authorization": f"Bot {self.__bot_token}"},
        )

    async def _get_current_auth_info(self, access_token: str) -> AuthInfo:
        return await self.request(
            Route("GET", "/oauth2/@me"),
            headers={"Authorization": f"Bearer {access_token}"},
        )
