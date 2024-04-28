from Crypto.Random import get_random_bytes
from uuid_extensions import uuid7

from app.crypto_fs.AES import AES


def uuid() -> int:
    return uuid7(as_type="int")


def as_str(uid: int) -> str:
    return f"{uid:x}"


def random_key() -> bytes:
    return get_random_bytes(AES.key_size)
