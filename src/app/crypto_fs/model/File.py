from dataclasses import dataclass, field
from typing import Literal

from app.crypto_fs.utility import uuid, random_key


@dataclass
class File:
    type: Literal["dir", "file"]
    uid: int = field(default_factory=uuid)
    key: bytes = field(default_factory=random_key)
