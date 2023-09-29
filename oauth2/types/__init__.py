from typing import List, Union

from typing_extensions import TypeAlias

from .appinfo import *
from .emoji import *
from .guild import *
from .payloads import *
from .role import *
from .sticker import *
from .team import *
from .user import *

Snowflake: TypeAlias = Union[str, int]
SnowflakeList: TypeAlias = Union[List[str], List[int]]
