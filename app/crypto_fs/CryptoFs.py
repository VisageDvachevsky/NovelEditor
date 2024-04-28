import pickle

from pathlib import Path
from Crypto.Random import get_random_bytes
from loguru import logger
from uuid_extensions import uuid7

from app.crypto_fs.AES import AES
from app.crypto_fs.model.Dir import Dir
from app.crypto_fs.model.File import File
from app.crypto_fs.model.Root import Root


class CryptoFs:
    def __init__(self, root_path: str, root: Root) -> None:
        self._root = root
        self._root_path = root_path
        Path(self._root_path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def uuid():
        return uuid7(as_type="int")

    @staticmethod
    def _as_str(uid: int):
        return f"{uid:x}"

    @staticmethod
    def random_key() -> bytes:
        return get_random_bytes(AES.key_size)

    def _read_bytes(self, uid: int, key: bytes) -> bytes | None:
        path = Path(self._root_path, self._as_str(uid))
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

    def _write_bytes(self, uid: int, key: bytes, data: bytes) -> None:
        path = Path(self._root_path, self._as_str(uid))
        data = AES(key).encrypt(data)
        path.write_bytes(data)

    def _read_obj_dir(self, uid: int, key: bytes) -> Dir | None:
        data = self._read_bytes(uid, key)
        if data is None:
            return None

        try:
            res: Dir = pickle.loads(data)
            return res
        except Exception as _:
            logger.error(f"Не удалось распаковать объект '{uid}'")

    def _read_dir(
        self, path: list[str], mkdir: bool = False
    ) -> tuple[Dir, int, bytes] | None:
        root = self._root

        uid = root.uid
        key = root.key
        dir = self._read_obj_dir(uid, key)

        for idx, part in enumerate(path):
            if dir is None:
                if not mkdir:
                    return None

                dir = Dir()
                self._write_bytes(uid, key, pickle.dumps(dir))

            file = dir.get(part)
            if file is None:
                if not mkdir:
                    logger.error(f"Путь '{path[:idx]}' не найден.")
                    return None

                file = File(
                    uid=self.uuid(),
                    key=self.random_key(),
                    type="dir",
                )
                dir[part] = file
                self._write_bytes(uid, key, pickle.dumps(dir))

            if file.type != "dir":
                logger.error(f"Путь '{path[:idx]}' не является директорией.")
                return None

            uid = file.uid
            key = file.key
            dir = self._read_obj_dir(uid, key)

        if dir is None and mkdir:
            dir = Dir()
            self._write_bytes(uid, key, pickle.dumps(dir))

        if dir is None:
            return None

        return dir, uid, key

    def read_dir(self, path: list[str] | str, mkdir: bool = False) -> Dir | None:
        if path is str:
            return self.read_dir(path.split("/"))

        res = self._read_dir(path, mkdir=mkdir)
        if res is None:
            return None

        return res[0]

    def read_file(self, path: list[str] | str) -> bytes | None:
        if path is str:
            return self.read_file(path.split("/"))

        dir = self.read_dir(path[:-1])
        if dir is None:
            return None

        filename = path[-1]
        file = dir.get(filename)
        if file is None:
            logger.error(f"Путь '{path}' не найден.")
            return None

        if file.type != "file":
            logger.error(f"Путь '{path} не является файлом.")
            return None

        data = self._read_bytes(file.uid, file.key)
        return data

    def write_file(self, path: list[str] | str, data: bytes, overwrite: bool = True):
        if path is str:
            return self.write_file(path.split("/"), data, overwrite=overwrite)

        dir = self._read_dir(path[:-1], mkdir=True)
        if dir is None:
            logger.error(f"Не удалось открыть папку '{path[:-1]}'.")
            return

        filename = path[-1]
        file = dir[0].get(filename)
        if file is not None and not overwrite:
            logger.warning(f"Путь '{path}' уже существует.")
            return

        if file is not None:
            self._remove(file)
        file = File(uid=self.uuid(), key=self.random_key(), type="file")
        self._write_bytes(file.uid, file.key, data)

        dir[0][filename] = file
        self._write_bytes(dir[1], dir[2], pickle.dumps(dir[0]))

    def _remove(self, file: File):
        path = Path(self._root_path, self._as_str(file.uid))

        if file.type == "dir":
            dir = self._read_obj_dir(file.uid, file.key)
            if dir is not None:
                for filename in dir:
                    self._remove(dir[filename])

        path.unlink(missing_ok=True)

    def remove(self, path: list[str] | str) -> None:
        if path is str:
            return self.remove(path.split("/"))

        dir = self._read_dir(path[:-1])
        if dir is None:
            logger.error(f"Не удалось открыть папку '{path[:-1]}'.")
            return

        filename = path[-1]
        if filename is None:
            logger.warning(f"Файл '{path}' не существует.")
            return

        file = dir[0].get(filename)
        if file is not None:
            self._remove(file)
            del dir[0][filename]
            self._write_bytes(dir[1], dir[2], pickle.dumps(dir[0]))
