import os
from io import BytesIO

from PIL import Image
from cryptography.fernet import Fernet

from app.image_manager.create_db import create_db


class ImageManager:
    def __init__(self, db_name="image_database.db", key_file="key.key"):
        self.images = create_db(db_name).image
        self.db_name = db_name
        self.key = self.load_or_create_key(key_file)

    @staticmethod
    def load_or_create_key(key_file):
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key

    def add_image(self, image_path, image_hash):
        if not os.path.isfile(image_path):
            print(f"Ошибка: Файл изображения '{image_path}' не найден.")
            return

        with open(image_path, "rb") as f:
            image_bytes = f.read()

            (
                self.images.insert(
                    image_hash=image_hash, image_data=self.encrypt_data(image_bytes)
                )
                .on_conflict_replace()
                .execute()
            )

            print(f"Изображение добавлено в базу данных.")

    def get_image_data(self, image_hash):
        try:
            img = self.images.get(self.images.image_hash == image_hash)
            if img:
                return self.decrypt_data(img.image_data)
        except Exception as _:
            print(f"Ошибка: Изображение не найдено в базе данных.")
            return None

    def get_image_hashes(self):
        return [res.image_hash for res in self.images.select()]

    def remove_image(self, image_hash):
        self.images.delete().where(self.images.image_hash == image_hash).execute()
        print(f"Изображение удалено из базы данных.")

    def encrypt_data(self, data):
        cipher = Fernet(self.key)
        return cipher.encrypt(data)

    def decrypt_data(self, encrypted_data):
        cipher = Fernet(self.key)
        return cipher.decrypt(encrypted_data)

    def backup_database(self, backup_file):
        with open(self.db_name, "rb") as f_src:
            with open(backup_file, "wb") as f_dest:
                f_dest.write(f_src.read())


class ProjectBuilder:
    def __init__(self, image_manager, project_name):
        self.image_manager = image_manager
        self.project_name = project_name

    def build_project(self, image_id):
        image_data = self.image_manager.get_image_data(image_id)
        if image_data:
            try:
                img = Image.open(BytesIO(image_data))
                img.show()
            except Exception as e:
                print(f"Ошибка при отображении изображения: {e}")
        else:
            print(f"Ошибка: Изображение с айди {image_id} не найдено в базе данных.")
