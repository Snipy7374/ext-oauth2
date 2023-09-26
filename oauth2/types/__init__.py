from typing_extensions import TypeAlias, Union

from .appinfo import *
from .emoji import *
from .payloads import *
from .team import *
from .user import *

Snowflake: TypeAlias = Union[str, int]
