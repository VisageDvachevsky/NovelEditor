import os

from loguru import logger

from app.crypto_fs.CryptoFs import CryptoFs
from app.crypto_fs.load_root import load_root


class ImageManager:
    def __init__(self, key_file="key.key"):
        self._fs = CryptoFs("data", load_root(key_file))

    def add_image(self, image_path, image_hash):
        if not os.path.isfile(image_path):
            logger.error(f"Файл изображения '{image_path}' не найден.")
            return

        with open(image_path, "rb") as f:
            image_bytes = f.read()

            self._fs.write_file(["images", image_hash], image_bytes)

            logger.info(f"Изображение добавлено в базу данных.")

    def get_image_data(self, image_hash):
        try:
            return self._fs.read_file(["images", image_hash])
        except Exception as _:
            logger.error(f"Изображение не найдено в базе данных.")
            return None

    def remove_image(self, image_hash):
        self._fs.remove(["images", image_hash])
        logger.info(f"Изображение удалено из базы данных.")

    def backup_database(self, backup_file):
        logger.warning(f"Действие недоступно!")
