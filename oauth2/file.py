from __future__ import annotations

import enum
import io
import os
from typing import Union

from typing_extensions import TypeAlias

FileLike: TypeAlias = Union[str, bytes, os.PathLike, io.BufferedIOBase]


class FileType(enum.Enum):
    png = "image/png"
    jpeg = "image/jpeg"
    gif = "image/gif"


class File:
    def __init__(self, fp: FileLike, file_type: FileType = FileType.png) -> None:
        if isinstance(fp, io.IOBase):
            if not (fp.seekable() and fp.readable()):
                raise ValueError(f"File buffer {fp!r} must be seekable and readable")
            self.fp = fp
            self._original_pos = fp.tell()
        else:
            self.fp = open(fp, "rb")
            self._original_pos = 0

        self.file_type = file_type
