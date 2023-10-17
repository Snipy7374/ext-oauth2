from typing import List, Union

from typing_extensions import TypeAlias

from .appinfo import *
from .connection import *
from .emoji import *
from .guild import *
from .i18n import *
from .integration import *
from .payloads import *
from .role import *
from .sticker import *
from .team import *
from .user import *
from .channel import *

Snowflake: TypeAlias = Union[str, int]
SnowflakeList: TypeAlias = Union[List[str], List[int]]
