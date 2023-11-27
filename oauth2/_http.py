from __future__ import annotations

import asyncio
import logging
import sys
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Tuple
from urllib.parse import quote as _uriquote

import aiohttp

from oauth2 import __version__
from oauth2.utils import _to_json

if TYPE_CHECKING:
    from oauth2.scopes import OAuthScopes
    from oauth2.types import (
        AccessExchangeTokenPayload,
        AccessTokenResponse,
        AppInfo,
        ApplicationRoleConnection,
        AppRoleConnectionPayload,
        AuthInfo,
        ClientCredentialsPayload,
        ClientCredentialsResponse,
        Connection,
        GetGuildsParams,
        PartialGuild,
        RefreshTokenPayload,
        RevokeTokenPayload,
        User,
        AddGuildMemberPayload,
        GroupDMChannel,
        CreateGroupDMPayload,
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

    async def request(self, route: Route, bearer: bool = True, **kwargs: Any) -> Any:
        method = route.method
        url = route.url

        payload: Dict[str, Any] = kwargs.get("payload") or {}  # type: ignore # guess what, idc
        params: Dict[str, Any] = kwargs.get("params") or {}

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

        if auth := kwargs.get("auth"):
            bearer = False
            auth = aiohttp.BasicAuth(str(self._client_id), self.__client_secret)
            _log.debug(
                "Authenticating a request using client credentials as Login and Password"
            )

        if bearer:
            headers["Authorization"] = f"Bearer {kwargs['access_token']}"

        if kwargs.get("json"):
            headers["Content-Type"] = "application/json"
            payload: str = _to_json(payload)

        async with self.__session.request(method, url, data=payload, headers=headers, auth=auth, params=params) as response:  # type: ignore
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
            Route("POST", "/oauth2/token"), payload=payload, bearer=False
        )

    async def _refresh_token(self, *, refresh_token: str) -> AccessTokenResponse:
        payload: RefreshTokenPayload = {
            "client_id": self._client_id,
            "client_secret": self.__client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        return await self.request(
            Route("POST", "/oauth2/token"), payload=payload, bearer=False
        )

    async def _revoke_token(self, *, token: str, token_type: str) -> None:
        payload: RevokeTokenPayload = {
            "client_id": self._client_id,
            "client_secret": self.__client_secret,
            "token": token,
            "token_type": token_type,
        }

        return await self.request(
            Route("POST", "/oauth2/token/revoke"), payload=payload, bearer=False
        )

    async def _get_client_credentials_token(
        self, scopes: OAuthScopes
    ) -> ClientCredentialsResponse:
        payload: ClientCredentialsPayload = {
            "grant_type": "client_credentials",
            "scope": scopes.as_client_credentials(),
        }

        return await self.request(
            Route("POST", "/oauth2/token"), payload=payload, auth=True
        )

    async def _get_app_info(self) -> AppInfo:
        return await self.request(
            Route("GET", "/oauth2/applications/@me"),
            headers={"Authorization": f"Bot {self.__bot_token}"},
            bearer=False,
        )

    async def _get_current_auth_info(self, access_token: str) -> AuthInfo:
        return await self.request(
            Route("GET", "/oauth2/@me"), access_token=access_token
        )

    async def _get_current_user(self, access_token: str) -> User:
        return await self.request(
            Route("GET", "/users/@me"),
            access_token=access_token,
        )

    async def _edit_user(
        self, username: Optional[str], avatar: Optional[str], access_token: str
    ) -> User:
        payload = {}

        if username:
            payload["username"] = username
        if avatar:
            payload["avatar"] = avatar

        return await self.request(
            Route("PATCH", "/users/@me"),
            payload=payload,
            json=True,
            access_token=access_token,
        )

    async def _get_user_guids(
        self,
        before: Optional[int],
        after: Optional[int],
        limit: int,
        with_counts: bool,
        access_token: str,
    ) -> List[PartialGuild]:
        params: GetGuildsParams = {"limit": limit, "with_counts": with_counts}

        if before:
            params["before"] = before
        if after:
            params["after"] = after

        return await self.request(
            Route("GET", "/users/@me/guilds"), params=params, access_token=access_token
        )

    async def _get_user_connections(self, access_token: str) -> List[Connection]:
        return await self.request(
            Route("GET", "/users/@me/connections"), access_token=access_token
        )

    async def _get_user_application_connection(
        self, application_id: int, access_token: str
    ) -> ApplicationRoleConnection:
        return await self.request(
            Route("GET", f"/users/@me/applications/{application_id}/role-connection"),
            access_token=access_token,
        )

    # TODO: finish the implementation https://discord.com/developers/docs/resources/user#update-user-application-role-connection
    async def _update_user_application_connection(
        self,
        application_id: int,
        platform_name: Optional[str],
        platform_username: Optional[str],
        metadata: ...,
        access_token: str,
    ) -> ApplicationRoleConnection:
        payload: AppRoleConnectionPayload = {}

        if platform_name:
            payload["platform_name"] = platform_name
        if platform_username:
            payload["platform_username"] = platform_username
        if metadata:
            payload["metadata"] = metadata

        return await self.request(
            Route("PUT", f"/users/@me/applications/{application_id}/role-connection"),
            payload=payload,
            json=True,
            access_token=access_token,
        )

    async def _get_guild_member(self, guild_id: int, access_token: str):
        return await self.request(
            Route("GET", f"/users/@me/guilds/{guild_id}/member"),
            access_token=access_token,
        )

    async def _add_guild_member(
        self,
        guild_id: int,
        user_id: int,
        nick: Optional[str],
        roles: List[int],
        mute: Optional[bool],
        deaf: Optional[bool],
        access_token: str,
    ) -> None:
        payload: AddGuildMemberPayload = {"access_token": access_token}

        if nick:
            payload["nick"] = nick
        if roles:
            payload["roles"] = roles  # type: ignore
        if mute:
            payload["mute"] = mute
        if deaf:
            payload["deaf"] = deaf

        return await self.request(
            Route("PUT", f"/guilds/{guild_id}/members/{user_id}"),
            bearer=False,
            headers={"Authorization": f"Bot {self.__bot_token}"},
            payload=payload,
            json=True,
        )

    async def _create_group_dm(
        self,
        access_tokens: List[str],
        nicks: Dict[int, str]
    ) -> GroupDMChannel:
        payload: CreateGroupDMPayload = {"access_tokens": access_tokens, "nicks": nicks}  # type: ignore
        return await self.request(
            Route("POST", "/users/@me/channels"),
            bearer=False,
            headers={"Authorization": f"Bot {self.__bot_token}"},
            payload=payload,
            json=True,
        )

    # the bot must be the gdm owner, see the postman requests
    async def _add_group_dm_user(
        self,
        channel_id: int,
        user_id: int,
        access_token: str,
        nick: str,
    ) -> None:
        payload = {"access_token": access_token, "nick": nick}
        return await self.request(
            Route("PUT", f"/channels/{channel_id}/recipients/{user_id}"),
            payload=payload,
            json=True,
            headers={"Authorization": f"Bot {self.__bot_token}"},
            bearer=False,
        )

    # same as above
    async def _remove_group_dm_user(
        self,
        channel_id: int,
        user_id: int,
    ) -> None:
        return await self.request(
            Route("DELETE", f"/channels/{channel_id}/recipients/{user_id}"),
            headers={"Authorization": f"Bot {self.__bot_token}"},
            bearer=False,
        )

