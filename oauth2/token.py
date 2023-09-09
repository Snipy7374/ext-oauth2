from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union

import attrs
import datetime

if TYPE_CHECKING:
    from .types import AccessTokenResponse, AccessTokenDict, ClientCredentialsResponse


def to_datetime(_v: str) -> datetime.datetime:
    s = int(_v)
    date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=s)
    return date


@attrs.define(slots=True, repr=True)
class AccessToken:
    access_token: str
    token_type: str
    expires_in: datetime.datetime = attrs.field(converter=to_datetime)
    refresh_token: Optional[str]
    scope: str

    @classmethod
    def from_data(cls, data: Union[AccessTokenResponse, ClientCredentialsResponse]) -> AccessToken:
        return cls(
            data["access_token"],
            data["token_type"],
            data["expires_in"],
            (
                data["refresh_token"] if "refresh_token" in data.keys()  # type: ignore
                else None  # type: ignore
            ),
            data["scope"],
        )

    def to_dict(self) -> AccessTokenDict:
        """A useful method to transform the data holded
        by the object to a dict.

        This is mostly useful when storing the data.
        Note that this method excludes falsy values.
        """
        return {
            k: v for k in self.__slots__
            if not k.startswith("__") and (v := self.__getattribute__(k)) # excluding dunder methods and falsy values
        }  # type: ignore
