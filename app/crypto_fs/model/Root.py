from dataclasses import dataclass, field

from app.crypto_fs.utility import uuid, random_key


@dataclass
class Root:
    uid: int = field(default_factory=uuid)
    key: bytes = field(default_factory=random_key)
