from dataclasses import dataclass
from typing import Literal


@dataclass
class File:
    uid: int
    type: Literal["dir", "file"]
    key: bytes
