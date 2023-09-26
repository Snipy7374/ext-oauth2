from __future__ import annotations

import enum
from typing import Any, Generator, Tuple

__all__: Tuple[str, ...] = ("OAuthScopes",)


class OAuthScopes(enum.IntFlag):
    activities_read = enum.auto()
    activities_write = enum.auto()
    applications_builds_read = enum.auto()
    applications_builds_upload = enum.auto()
    applications_commands = enum.auto()
    applications_commands_update = enum.auto()
    applications_commands_permissions_update = enum.auto()
    applications_entitlements = enum.auto()
    applications_store_update = enum.auto()
    bot = enum.auto()
    connections = enum.auto()
    dm_channels_read = enum.auto()
    email = enum.auto()
    gdm_join = enum.auto()
    guilds = enum.auto()
    guilds_join = enum.auto()
    guilds_members_read = enum.auto()
    identify = enum.auto()
    messages_read = enum.auto()
    relationships_read = enum.auto()
    role_connections_write = enum.auto()
    rpc = enum.auto()
    rpc_activities_write = enum.auto()
    rpc_notifications_read = enum.auto()
    rpc_voice_read = enum.auto()
    rpc_voice_write = enum.auto()
    voice = enum.auto()
    webhook_incoming = enum.auto()

    def __iter__(self) -> Generator[OAuthScopes, Any, None]:
        cls = type(self)
        n = self.value

        while n:
            b = n & -n
            yield cls(b)
            n ^= b

    @property
    def api_name(self) -> str:
        # i need to check for this since discord is inconsistent
        # with scope names (sigh)
        if self._name_.startswith(("role_connections", "dm_channels")):
            _name_chars = list(self._name_)
            under = self._name_.rfind("_")
            _name_chars[under] = "."
            return "".join(_name_chars)

        if self._name_:
            return self._name_.replace("_", ".")

        raise RuntimeError("This is a library bug.")  # Should never happen

    @classmethod
    def none(cls) -> OAuthScopes:
        return cls(0)

    def as_url_param(self) -> str:
        return "%20".join(scope.api_name for scope in self)
