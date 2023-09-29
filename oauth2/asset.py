from __future__ import annotations

import io
import os
from typing import TYPE_CHECKING, ClassVar, Union

import attrs
from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from oauth2._http import HTTPClient

FileLike: TypeAlias = Union[str, bytes, os.PathLike, io.BufferedIOBase]


@attrs.define(slots=True, repr=True)
class Asset:
    BASE: ClassVar[str] = "https://cdn.discordapp.com"
    url: str
    key: str
    animated: bool
    _http: HTTPClient

    async def read(self) -> bytes:
        return await self._http.get_from_cdn(self.url)

    async def save(self, fp: FileLike, *, seek_begin: bool) -> int:
        data = await self.read()
        if isinstance(fp, io.BufferedIOBase):
            written = fp.write(data)
            if seek_begin:
                fp.seek(0)
            return written
        else:
            with open(fp, "wb") as f:
                return f.write(data)

    @classmethod
    def _from_default_avatar(cls, http: HTTPClient, index: int) -> Asset:
        return cls(
            url=f"{cls.BASE}/embed/avatars/{index}.png",
            key=str(index),
            animated=False,
            _http=http,
        )

    @classmethod
    def _from_avatar(cls, http: HTTPClient, user_id: int, avatar: str) -> Asset:
        animated = avatar.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{cls.BASE}/avatars/{user_id}/{avatar}.{format}?size=1024",
            key=avatar,
            animated=animated,
            _http=http,
        )

    @classmethod
    def _from_guild_avatar(
        cls, http: HTTPClient, guild_id: int, member_id: int, avatar: str
    ) -> Asset:
        animated = avatar.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{cls.BASE}/guilds/{guild_id}/users/{member_id}/avatars/{avatar}.{format}?size=1024",
            key=avatar,
            animated=animated,
            _http=http,
        )

    @classmethod
    def _from_icon(
        cls, http: HTTPClient, object_id: int, icon_hash: str, path: str
    ) -> Asset:
        return cls(
            url=f"{cls.BASE}/{path}-icons/{object_id}/{icon_hash}.png?size=1024",
            key=icon_hash,
            animated=False,
            _http=http,
        )

    @classmethod
    def _from_cover_image(
        cls, http: HTTPClient, object_id: int, cover_image_hash: str
    ) -> Asset:
        return cls(
            url=f"{cls.BASE}/app-assets/{object_id}/store/{cover_image_hash}.png?size=1024",
            key=cover_image_hash,
            animated=False,
            _http=http,
        )

    @classmethod
    def _from_guild_image(
        cls, http: HTTPClient, guild_id: int, image: str, path: str
    ) -> Asset:
        return cls(
            url=f"{cls.BASE}/{path}/{guild_id}/{image}.png?size=1024",
            key=image,
            animated=False,
            _http=http,
        )

    @classmethod
    def _from_guild_icon(cls, http: HTTPClient, guild_id: int, icon_hash: str) -> Asset:
        animated = icon_hash.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{cls.BASE}/icons/{guild_id}/{icon_hash}.{format}?size=1024",
            key=icon_hash,
            animated=animated,
            _http=http,
        )

    @classmethod
    def _from_banner(cls, http: HTTPClient, id: int, banner_hash: str) -> Asset:
        animated = banner_hash.startswith("a_")
        format = "gif" if animated else "png"
        return cls(
            url=f"{cls.BASE}/banners/{id}/{banner_hash}.{format}?size=1024",
            key=banner_hash,
            animated=animated,
            _http=http,
        )

    @classmethod
    def _from_avatar_decoration(
        cls, http: HTTPClient, id: int, avatar_decoration_hash: str
    ) -> Asset:
        return cls(
            url=f"{cls.BASE}/avatar-decorations/{id}/{avatar_decoration_hash}.png?size=1024",
            key=avatar_decoration_hash,
            animated=False,
            _http=http,
        )
