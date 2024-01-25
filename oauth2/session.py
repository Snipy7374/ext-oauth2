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
    """A class that represents and holds informations
    about an OAuth2 user authorization given to your application.

    Attributes
    ----------
    access_token: :class:`str`
        The user's access token. Used or required by the library for
        some actions on users.
    token_type: :class:`str`
        The type of the token. For example this can be ``bearer``...
    expires_in: :class:`datetime.datetime`
        The date when the user's ``access_token`` will expire.
    scope
    state_code: Optional[:class:`str`]
        The security state string used when the user's
        authorized your application, if any.
    refresh_token: Optional[:class:`str`]
        The token that should be used to refresh the current token.
        You may want to refresh a token when the ``access_token`` is expiring
        or if you had a data breach in your application.
    guild_id: Optional[:class:`int`]
        The id of the guild that your bot joined when it was authorized by the user.

        .. note::
            This is available only when :attr:`OAuthScopes.bot` is passed to the
            client scopes.

    permissions: Optional[:class:`int`]
        The permissions that your bot was granted when it was authorized by the user.

        .. note::
            This is available only when :attr:`OAuthScopes.bot` is passed to the
            client scopes.
    """

    access_token: str
    token_type: str
    expires_in: datetime.datetime = attrs.field(converter=to_datetime)
    scope: str
    _client: Client
    state_code: Optional[str] = None
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
        """Create an OAuth2Session object from discord's payloads.

        .. note::
            This is intended to be used when using the :attr:`ResponseType.token` authorization flow. If you're using the :attr:`ResponseType.code` authorization flow the library authomatically creates the OAuth2Session object after exchanging the ``code`` with discord.

        Parameters
        ----------
        data: Union[:class:`AccessTokenResponse`, :class:`ClientCredentialsResponse`]
            The data that you got from discord after the user's authorization.
        state: Optional[:class:`Str`]
            The security state string, if any.
        client: :class:`Client`
            The client object which is managing this session.

        Returns
        -------
        :class:`OAuth2Session`
            The OAuth2Session object from the parameters payloads.
        """
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
        """:class:`Client`: returns the client object."""
        return self._client

    @property
    def is_expired(self) -> bool:
        """:class:`bool`: whether the ``access_token`` expired or not."""
        return (
            datetime.datetime.now(datetime.timezone.utc)
        ).timestamp() >= self.expires_in.timestamp()

    async def refresh(self) -> None:
        """Refresh the ``access_token`` using the ``refresh_token``.

        .. note::
            This is an in-place method, so the current object where this method is called will be updated with new token-related informations making the old ones lost forever.
        """
        if not self.refresh_token:
            raise ValueError(
                f"Couldn't refresh the token because {self.refresh_token!r}"
            )
        data = await self._client.http._refresh_token(refresh_token=self.refresh_token)
        self._update(data)

    async def revoke(self) -> None:
        """Revoke the ``access_token``.

        .. note::
            This method, unlike :meth:`.refresh`, doesn't update the current object.
        """
        await self._client.http._revoke_token(
            token=self.access_token, token_type=self.token_type
        )
        self.client._remove_oauth2_session(self)

    async def fetch_current_authorization_info(self) -> AuthorizationInfo:
        """Fetch the authorization info linked to this OAuth2 session.

        Returns
        -------
        :class:`AuthorizationInfo`
            The authorization information liked to this session.
        """
        data = await self._client.http._get_current_auth_info(self.access_token)
        return AuthorizationInfo.from_data(data, self._client.http, self)

    async def fetch_current_user(self) -> User:
        """Fetch the user associated to this OAuth2 session.

        Returns
        -------
        :class:`User`
            The user associated to this OAuth2 session.
        """
        data = await self._client.http._get_current_user(self.access_token)
        return User.from_data(data, self._client.http, self)

    async def add_current_user_to_group_dm(
        self,
        channel_id: int,
        *,
        user_id: Optional[int] = None,
        nick: Optional[str] = None,
    ) -> None:
        if not user_id:
            user = await self.fetch_current_user()

        await self._client.http._add_group_dm_user(
            channel_id,
            user_id if user_id else user.id,
            self.access_token,
            nick if nick else user.username,
        )

    async def remove_current_user_from_group_dm(
        self, channel_id: int, *, user_id: Optional[int] = None
    ) -> None:
        if not user_id:
            user = await self.fetch_current_user()

        await self._client.http._remove_group_dm_user(
            channel_id, user_id if user_id else user.id
        )
