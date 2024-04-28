from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES as CRYPTO_AES
from Crypto.Util.Padding import pad, unpad


class AES:
    key_size = CRYPTO_AES.key_size[2]
    _bs = CRYPTO_AES.block_size

    def __init__(self, key: bytes):
        self._key = key

    def encrypt(self, data: bytes) -> bytes:
        raw = pad(data, self._bs)
        iv = get_random_bytes(self._bs)
        cipher = CRYPTO_AES.new(self._key, CRYPTO_AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        iv = encrypted_data[: self._bs]
        data = encrypted_data[self._bs :]
        cipher = CRYPTO_AES.new(self._key, CRYPTO_AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(data), self._bs)
