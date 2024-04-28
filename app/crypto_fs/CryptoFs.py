import pickle

from loguru import logger

from app.crypto_fs.RawCryptoFs import RawCryptoFs
from app.crypto_fs.model.Dir import Dir
from app.crypto_fs.model.File import File
from app.crypto_fs.model.Root import Root


class CryptoFs:
    def __init__(self, root_path: str, root: Root) -> None:
        self._root = root
        self._fs = RawCryptoFs(root_path)

    def _read_dir(
        self, path: list[str], mkdir: bool = False
    ) -> tuple[Dir, int, bytes] | None:
        uid = self._root.uid
        key = self._root.key
        dir: Dir = self._fs.read_pickle(uid, key)

        for idx, part in enumerate(path):
            if dir is None:
                if not mkdir:
                    return None

                dir = Dir()
                self._fs.write_bytes(uid, key, pickle.dumps(dir))

            file = dir.get(part)
            if file is None:
                if not mkdir:
                    logger.error(f"Путь '{path[:idx]}' не найден.")
                    return None

                file = File(type="dir")
                dir[part] = file
                self._fs.write_bytes(uid, key, pickle.dumps(dir))

            if file.type != "dir":
                logger.error(f"Путь '{path[:idx]}' не является директорией.")
                return None

            uid = file.uid
            key = file.key
            dir = self._fs.read_pickle(uid, key)

        if dir is None and mkdir:
            dir = Dir()
            self._fs.write_bytes(uid, key, pickle.dumps(dir))

        if dir is None:
            return None

        return dir, uid, key

    def read_dir(self, path: list[str], mkdir: bool = False) -> Dir | None:
        res = self._read_dir(path, mkdir=mkdir)
        if res is None:
            return None

        return res[0]

    def read_file(self, path: list[str]) -> bytes | None:
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

        data = self._fs.read_bytes(file.uid, file.key)
        return data

    def write_file(self, path: list[str], data: bytes, overwrite: bool = True):
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
        file = File(type="file")
        self._fs.write_bytes(file.uid, file.key, data)

        dir[0][filename] = file
        self._fs.write_bytes(dir[1], dir[2], pickle.dumps(dir[0]))

    def _remove(self, file: File):
        if file.type == "dir":
            dir: Dir = self._fs.read_pickle(file.uid, file.key)
            if dir is not None:
                for dir_file in dir.values():
                    self._remove(dir_file)

        self._fs.remove(file.uid)

    def remove(self, path: list[str] | str) -> None:
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
            self._fs.write_bytes(dir[1], dir[2], pickle.dumps(dir[0]))
