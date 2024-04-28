import pickle

from pathlib import Path
from typing import Any

from loguru import logger

from app.crypto_fs.AES import AES
from app.crypto_fs.utility import as_str


class RawCryptoFs:
    def __init__(self, root_path: str) -> None:
        self._root_path = root_path
        Path(self._root_path).mkdir(parents=True, exist_ok=True)

    def _as_path(self, uid: int) -> Path:
        return Path(self._root_path, as_str(uid))

    def read_bytes(self, uid: int, key: bytes) -> bytes | None:
        path = self._as_path(uid)
        if not path.exists():
            logger.error(f"Объект '{uid}' не существует")
            return None

        try:
            edata = path.read_bytes()
            data = AES(key).decrypt(edata)
            return data
        except Exception as _:
            logger.error(f"Не удалось расшифровать объект '{path}'.")
            return None

    def write_bytes(self, uid: int, key: bytes, data: bytes) -> None:
        path = self._as_path(uid)
        data = AES(key).encrypt(data)
        path.write_bytes(data)

    def read_pickle(self, uid: int, key: bytes) -> Any | None:
        data = self.read_bytes(uid, key)
        if data is None:
            return None

        try:
            res = pickle.loads(data)
            return res
        except Exception as _:
            logger.error(f"Не удалось распаковать объект '{uid}'")

    def write_pickle(self, uid: int, key: bytes, data: Any) -> None:
        self.write_bytes(uid, key, pickle.dumps(data))

    def remove(self, uid: int):
        self._as_path(uid).unlink(missing_ok=True)
