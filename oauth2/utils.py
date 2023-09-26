from __future__ import annotations
from typing import Optional, TYPE_CHECKING, List

import datetime

if TYPE_CHECKING:
    from oauth2.scopes import OAuthScopes
    from oauth2.appinfo import InstallParams
    from oauth2.types import InstallParams as InstallParamsPayload


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
