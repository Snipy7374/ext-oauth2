from typing import Tuple, TypedDict

__all__: Tuple[str, ...] = ("ExchangeTokenPayload",)


class ExchangeTokenPayload(TypedDict):
    client_id: int
    client_secret: str
    grant_type: str
    code: str
    redirect_uri: str
