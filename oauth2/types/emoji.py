from typing import TypedDict, Tuple


__all__: Tuple[str, ...] = ("EmojiData",)


class EmojiData(TypedDict):
    hoist: bool
    name: str
    mentionable: bool
    color: int
    position: int
    id: int
    managed: bool
    permissions: int
    permissions_new: int
