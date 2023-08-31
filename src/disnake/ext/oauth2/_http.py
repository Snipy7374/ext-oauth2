import asyncio
import sys
from typing import Any, Optional, Tuple

import aiohttp
from disnake.http import HTTPClient, Route
from disnake.utils import MISSING

from disnake.ext.oauth2 import __version__

__all__: Tuple[str, ...] = ("HTTP",)


class HTTP(HTTPClient):
    def __init__(
        self,
        connector: Optional[aiohttp.BaseConnector],
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        super().__init__(connector, loop=loop)

        self.user_agent = f"DiscordApp (https://github.com/Snipy7374/disnake-ext-oauth2 {__version__}) Python/{(py_ver:=sys.version_info)[0]}.{py_ver[1]} aiohttp/{aiohttp.__version__}"

    async def create_session(self) -> None:
        self.__session = aiohttp.ClientSession(connector=self.connector)

    async def request(self, route: Route, **kwargs: Any) -> Any:
        if self.__session is MISSING:
            await self.create_session()
