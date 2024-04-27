import os

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class Crypt:
    def __init__(self, key_file="key.key"):
        self._bs = AES.block_size
        self._key = self._load_or_create_key(key_file)

    @staticmethod
    def _load_or_create_key(key_file: str) -> bytes:
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()

        key = get_random_bytes(AES.key_size[2])
        with open(key_file, "wb") as f:
            f.write(key)
        return key

    def encrypt_data(self, data: bytes) -> bytes:
        raw = pad(data, self._bs)
        iv = get_random_bytes(self._bs)
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        iv = encrypted_data[: self._bs]
        data = encrypted_data[self._bs :]
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(data), self._bs)
