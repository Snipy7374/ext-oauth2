from __future__ import annotations

import base64
from typing import TYPE_CHECKING, AsyncIterator, List, Optional

import attrs

from oauth2.asset import Asset
from oauth2.connection import (
    ApplicationRoleConnection,
    ApplicationRoleConnectionMetadata,
    Connection,
)
from oauth2.guild import PartialGuild

if TYPE_CHECKING:
    from oauth2._http import HTTPClient
    from oauth2.file import File
    from oauth2.session import OAuth2Session
    from oauth2.types import User as UserData
    from oauth2.types import PartialDMUser


@attrs.define(slots=True, repr=True)
class User:
    _http: HTTPClient
    id: int
    username: str
    discriminator: str  # deprecation will happen soon
    bot: bool
    system: bool
    mfa_enabled: bool
    verified: bool
    _public_flags: int
    premium_type: int
    _session: Optional[OAuth2Session]
    locale: Optional[str] = None
    _avatar_decoration: Optional[str] = None
    email: Optional[str] = None
    global_name: Optional[str] = None
    _avatar: Optional[str] = None
    _banner: Optional[str] = None
    _accent_colour: Optional[str] = None

    @classmethod
    def from_data(
        cls,
        data: UserData | PartialDMUser,
        http: HTTPClient,
        session: Optional[OAuth2Session] = None,
    ) -> User:
        return cls(
            _http=http,
            id=data["id"],  # type: ignore
            username=data["username"],
            discriminator=data["discriminator"],
            bot=data.get("bot", False),
            system=data.get("system", False),
            mfa_enabled=data.get("mfa_enabled", False),
            _session=session,
            locale=data.get("locale"),
            verified=data.get("verified", False),
            _public_flags=data.get("public_flags", 0),
            premium_type=data.get("premium_type", 0),
            _avatar=data.get("avatar"),
            _banner=data.get("banner"),
            _accent_colour=data.get("accent_colour"),
        )

    @property
    def default_avatar(self) -> Asset:
        if self.discriminator == "0":
            index = (self.id >> 22) % 6
        else:
            # legacy behavior
            index = int(self.discriminator) % 5
        return Asset._from_default_avatar(self._http, index)

    @property
    def avatar(self) -> Optional[Asset]:
        if self._avatar:
            return Asset._from_avatar(self._http, self.id, self._avatar)

    @property
    def banner(self) -> Optional[Asset]:
        if self._banner:
            return Asset._from_banner(self._http, self.id, self._banner)

    @property
    def avatar_decoration(self) -> Optional[Asset]:
        if self._avatar_decoration:
            return Asset._from_avatar_decoration(
                self._http, self.id, self._avatar_decoration
            )

    @property
    def session(self) -> Optional[OAuth2Session]:
        if self._session:
            return self._session

    async def _avatar_helper(self, file: Optional[File] = None) -> Optional[str]:
        if not file:
            return

        data = self._http.loop.run_in_executor(None, file.fp.read)
        await data
        encoded_bytes = base64.b64encode(data.result())

        return f"data:{file.file_type};base64,{encoded_bytes}"

    async def edit(
        self, username: Optional[str] = None, avatar: Optional[File] = None
    ) -> User:
        if not self._session:
            raise AttributeError(
                "This user object can't be edited because it doesn't have a `session` linked."
            )

        avatar_data = await self._avatar_helper(avatar)
        data = await self._http._edit_user(
            username, avatar_data, self._session.access_token
        )
        return User.from_data(data, self._http, self._session)

    async def guilds(
        self,
        *,
        before: Optional[int] = None,
        after: Optional[int] = None,
        limit: int = 200,
        with_counts: bool = False,
    ) -> AsyncIterator[PartialGuild]:
        if not self._session:
            raise AttributeError(
                "This user object can't be edited because it doesn't have a `session` linked."
            )

        data = await self._http._get_user_guids(
            before, after, limit, with_counts, self._session.access_token
        )
        for i in data:
            yield PartialGuild.from_data(i, self._http)

    async def fetch_user_connections(self) -> List[Connection]:
        if not self._session:
            raise AttributeError(
                "This user object can't be edited because it doesn't have a `session` linked."
            )

        data = await self._http._get_user_connections(
            access_token=self._session.access_token
        )
        return [Connection.from_data(i) for i in data]

    async def fetch_user_application_role_connection(
        self, application_id: int
    ) -> ApplicationRoleConnection:
        if not self._session:
            raise AttributeError(
                "This user object can't be edited because it doesn't have a `session` linked."
            )

        data = await self._http._get_user_application_connection(
            application_id=application_id, access_token=self._session.access_token
        )
        return ApplicationRoleConnection.from_data(data)

    async def update_user_application_role_connection(
        self,
        application_id: int,
        platform_name: Optional[str] = None,
        platform_username: Optional[str] = None,
        metadata: Optional[ApplicationRoleConnectionMetadata] = None,
    ) -> ApplicationRoleConnection:
        if not self._session:
            raise AttributeError(
                "This user object can't be edited because it doesn't have a `session` linked."
            )

        data = await self._http._update_user_application_connection(
            application_id=application_id,
            platform_name=platform_name,
            platform_username=platform_username,
            metadata=metadata.to_dict() if metadata else None,
            access_token=self._session.access_token,
        )
        return ApplicationRoleConnection.from_data(data)
