import os

from cryptography.fernet import Fernet


class Crypto:
    def __init__(self, key_file="key.key"):
        key = self._load_or_create_key(key_file)
        self._cipher = Fernet(key)

    @staticmethod
    def _load_or_create_key(key_file: str) -> bytes:
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key

    def encrypt_data(self, data: bytes) -> bytes:
        return self._cipher.encrypt(data)

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        return self._cipher.decrypt(encrypted_data)
