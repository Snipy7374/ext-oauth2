from __future__ import annotations

import asyncio
import collections
import logging
import secrets
from typing import Optional, Tuple, List, Dict

import aiohttp

from oauth2._http import HTTPClient
from oauth2.appinfo import AppInfo
from oauth2.scopes import OAuthScopes
from oauth2.session import OAuth2Session
from oauth2.utils import PromptType, ResponseType, get_oauth2_url

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
        max_states_cache: int = 1000,
    ) -> None:
        """Represets a client connection that connects to Discord.
        This class is used to interact with the Discord OAuth2 API endpoints.

        Parameters
        ----------
        scopes: :class:`OAuthScopes`
            The scopes that this OAuth2 application requires to work.
        client_secret: :class:`str`
        redirect_uri: class:`str`
            The url link to use when redirecting the user after a successful login with discord.
        bot_token: Optional[:class:`str`]
            The token of the bot linked to the application. This may be needed dependeing on what functions you need to use. Generally you don't need to pass this parameter.
        connector: Optional[:class:`aiohttp.BaseConnector`]
            The connector to use for connection pooling.
        loop: Optional[:class:`asyncio.AbstractEventLoop`]
            The :class:`asyncio.AbstractEventLoop` to use for asynchronous operations.
            Defaults to ``None``, in which case the default event loop is used via
            :func:`asyncio.get_event_loop()`.
        max_states_cache: :class:`int`
            The maximum number of security states strings to cache.

        Attributes
        ----------
        client_id: :class:`int`
            The id of the OAuth2 application.
        redirect_uri: :class:`str`
            The url link to use when redirecting the user after a successful login with discord.
        scopes: :class:`OAuthScopes`
            The scopes that the client uses.
        loop: :class:`asyncio.AbstractEventLoop`
            The event loop that the client uses for asynchronous operations.
        """
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.__oauth2_sessions: List[OAuth2Session] = []
        self.__states: collections.deque[str] = collections.deque(
            maxlen=max_states_cache
        )

        # should raise a deprecation warning
        self.loop = loop or asyncio.get_event_loop()
        self.http = HTTPClient(
            connector,
            self.loop,
            client_id=client_id,
            client_secret=client_secret,
            bot_token=bot_token,
        )

    @property
    def oauth2_sessions(self) -> Tuple[OAuth2Session, ...]:
        """Tuple[:class:`OAuth2Session`]: Returns a tuple containing the active sessions managed by this client.

        .. note::
            This is populated only if you use the :attr:`ResponseType.code` authorization flow. Otherwise you should handle its population when receiving the ``access_token``.
            You can handle its population subclassig the :class:`Client` class and creating your custom methods.
        """
        return tuple(self.__oauth2_sessions)

    def _remove_oauth2_session(self, _session: OAuth2Session) -> None:
        self.__oauth2_sessions.remove(_session)

    @property
    def states(self) -> Tuple[str, ...]:
        """Tuple[:class:`str`]: Returns the generated string states.
        These are the security strings passed when logging-in users.

        For more information about this read https://discord.com/developers/docs/topics/oauth2#state-and-security
        """
        # find a way to create an hyperlink
        return tuple(self.__states)

    async def generate_state_link(
        self,
        permissions: Optional[int] = None,
        guild_id: Optional[int] = None,
        disable_guild_select: bool = False,
        response_type: ResponseType = ResponseType.code,
        prompt: PromptType = PromptType.consent,
    ) -> str:
        """Generate an invite link for a user to log-in.
        This function is useful to create invite links dynamically.

        Parameters
        ----------
        permissions: Optional[:class:`int`]
            The permissions required for the bot to operate.

            .. note:
                This does something only if the :attr:`OAuthScopes.bot`
                scope is active, otherwise it's ignored by the Discord API.

        guild_id: Optional[:class:`int`]
            The id of the guild where the bot should be added.

            .. note:
                This does something only if the :attr:`OAuthScopes.bot`
                scope is active, otherwise it's ignored by the Discord API.

        disable_guild_select: :class:`bool`
            Whether to allow the user to select a guild freely when inviting
            the bot.
        response_type: :class:`ResponseType`
            The response type to use. If set to :attr:`ResponseType.code` you will get a code to exchange for a token, otherwise you'll directly get an ``access_token`` without the needs to exchange the code.
            It's reccomended to use the exchange code flow.
        prompt: :class:`PromptType`
            Controls how the authorization flow handles existing authorizations.
            If a user has previously authorized your application with the requested scopes and ``prompt`` is set to :attr:`PromptType.consent`, it will request them to reapprove their authorization.
            If set to :attr:`PromptType.none`, it will skip the authorization screen and redirect them back to your redirect URI without requesting their authorization.

            .. note::
                For passthrough scopes, like :attr:`OAuthScopes.bot` and :attr:`OAuthScopes.webhook_incoming`, authorization is always required.

        Returns
        -------
        :class:`str`
            The authorization link that the user should use
            to authorize your application.
        """
        # implementation of state for security reasons
        # https://discord.com/developers/docs/topics/oauth2#state-and-security
        state_future = self.loop.run_in_executor(None, secrets.token_urlsafe, 32)
        await state_future

        state = state_future.result()
        self.__states.append(state)

        return get_oauth2_url(
            client_id=self.client_id,
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
            response_type=response_type,
            state=state,
            prompt=prompt,
            permissions=permissions,
            guild_id=guild_id,
            disable_guild_select=disable_guild_select,
        )

    async def exchange_code(
        self, code: str, state: Optional[str] = None
    ) -> OAuth2Session:
        """Exchange the security code to get
        the user's access token. This should be used only
        if the log-in with discord link had the ``response_type``
        setted to ``code``.

        Parameters
        ----------
        code: :class:`str`
            The security code that discord sent to you.
        state: Optional[:class:`str`]
            The security ``state`` string, if any.
        """
        # validate the state
        if state:
            # this state wasn't generated by us!
            if state not in self.__states:
                raise

        data = await self.http._exchange_token(
            code=code, redirect_uri=self.redirect_uri
        )
        session = OAuth2Session.from_data(data, state, self)
        self.oauth2_sessions.append(session)
        return session

    async def fetch_client_credentials_token(self) -> OAuth2Session:
        """Get the access token of the application owner using the client id and the client secret.

        .. warning::
            Meant to be used only for testing purpouses. Be careful with your ``client_id`` and ``client_secret`` because **anyone** could be able to fetch your access token through them.
        """
        data = await self.http._get_client_credentials_token(self.scopes)
        session = OAuth2Session.from_data(data, None, self)
        self.oauth2_sessions.append(session)
        return session

    async def fetch_application_info(self) -> AppInfo:
        """Fetch the application information from the Discord API.

        Returns
        -------
        :class:`AppInfo`
            An object representing the application's information.
        """
        data = await self.http._get_app_info()
        return AppInfo.from_data(data, self.http)

    async def create_group_dm(self, access_tokens: List[str], nicks: Dict[int, str]):
        data = await self.http._create_group_dm(access_tokens, nicks)
