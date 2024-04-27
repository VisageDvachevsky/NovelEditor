import os

from Crypto.Random import get_random_bytes


def load_or_create_key(key_file: str, key_size: int) -> bytes:
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()

    key = get_random_bytes(key_size)
    with open(key_file, "wb") as f:
        f.write(key)
    return key
