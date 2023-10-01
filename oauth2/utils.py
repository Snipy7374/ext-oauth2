from __future__ import annotations

import datetime
import json
from typing import TYPE_CHECKING, Any, List, Literal, Optional
from urllib.parse import urlencode

from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from oauth2.appinfo import InstallParams
    from oauth2.scopes import OAuthScopes
    from oauth2.types import InstallParams as InstallParamsPayload

BASE_OAUTH_AUTHORIZE_URL = "https://discord.com/oauth2/authorize?"
ResponseTypes: TypeAlias = Literal["code", "token"]
PromptTypes: TypeAlias = Literal["consent", "none"]


def _to_json(obj: Any) -> str:
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=True)


def get_oauth2_url(
    client_id: int,
    scopes: OAuthScopes,
    redirect_uri: str,
    permissions: Optional[int] = None,
    guild_id: Optional[int] = None,
    disable_guild_select: bool = False,
    response_type: ResponseTypes = "code",
    state: Optional[str] = None,
    prompt: PromptTypes = "consent",
) -> str:
    url = f"https://discord.com/oauth2/authorize?client_id={client_id}"
    if scopes:
        url += f"&scope={scopes.as_url_param()}"
    if permissions is not None:
        url += f"&permissions={permissions}"
    if guild_id is not None:
        url += f"&guild_id={guild_id}"
    url += f"&response_type={response_type}&" + urlencode(
        {"redirect_uri": redirect_uri}
    )
    if disable_guild_select:
        url += "&disable_guild_select=true"
    if state:
        url += f"&state={state}"
    url += f"&prompt={prompt}"
    return url


def _to_oauth2_scopes(_v: List[str]) -> OAuthScopes:
    from oauth2.scopes import OAuthScopes

    for i in _v:
        if i.startswith(("role_connections", "dm_channels")):
            _name_chars = list(i)
            under = i.rfind("_")
            _name_chars[under] = "."
            old_idx = _v.index(i)
            _v[old_idx] = "".join(_name_chars)
        else:
            i_ = i.replace(".", "_")
            old_idx = _v.index(i)
            _v[old_idx] = i_

    members = iter(_v)
    first_s = next(members)
    scopes = OAuthScopes[first_s]

    for scope in members:
        scopes |= OAuthScopes[scope]
    return scopes


def _to_install_params(_v: Optional[InstallParamsPayload]) -> Optional[InstallParams]:
    if _v is None:
        return

    from oauth2.appinfo import InstallParams

    scopes = _to_oauth2_scopes(_v["scopes"]) or OAuthScopes.none()
    return InstallParams(scopes, int(_v["permissions"]))


def to_datetime(_v: str) -> datetime.datetime:
    s = int(_v)
    date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=s)
    return date


def to_int(_v: Optional[str]) -> Optional[int]:
    if _v is None:
        return
    return int(_v)
