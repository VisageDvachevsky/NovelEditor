import os
import shutil

from app.image_manager.Crypto import Crypto
from app.image_manager.create_db import create_db


class ImageManager:
    def __init__(self, db_name="image_database.db", key_file="key.key"):
        self._images = create_db(db_name).image
        self._db_name = db_name
        self._crypto = Crypto(key_file)

    def add_image(self, image_path, image_hash):
        if not os.path.isfile(image_path):
            print(f"Ошибка: Файл изображения '{image_path}' не найден.")
            return

        with open(image_path, "rb") as f:
            image_bytes = f.read()

            (
                self._images.insert(
                    image_hash=image_hash,
                    image_data=self._crypto.encrypt_data(image_bytes),
                )
                .on_conflict_replace()
                .execute()
            )

            print(f"Изображение добавлено в базу данных.")

    def get_image_data(self, image_hash):
        try:
            img = self._images.get(self._images.image_hash == image_hash)
            if img:
                return self._crypto.decrypt_data(img.image_data)
        except Exception as _:
            print(f"Ошибка: Изображение не найдено в базе данных.")
            return None

    def remove_image(self, image_hash):
        self._images.delete().where(self._images.image_hash == image_hash).execute()
        print(f"Изображение удалено из базы данных.")

    def backup_database(self, backup_file):
        shutil.copyfile(self._db_name, backup_file)
