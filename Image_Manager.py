import sqlite3
import os
import base64
import uuid
from cryptography.fernet import Fernet
from PIL import Image
from io import BytesIO
import hashlib

class ImageManager:
    def __init__(self, db_name='image_database.db', key_file='key.key'):
        self.db_name = db_name
        self.key = self.load_or_create_key(key_file)
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

        os.chmod(self.db_name, 0o600)

    def load_or_create_key(self, key_file):
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                            image_hash TEXT PRIMARY KEY,
                            image_data BLOB
                          )''')
        self.conn.commit()

    def add_image(self, image_path, image_hash):
        if not os.path.isfile(image_path):
            print(f"Ошибка: Файл изображения '{image_path}' не найден.")
            return

        with open(image_path, 'rb') as f:
            image_bytes = f.read()

            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO images (image_hash, image_data) VALUES (?, ?)",
                           (image_hash, self.encrypt_data(image_bytes)))
            self.conn.commit()
            print(f"Изображение добавлено в базу данных.")

    def get_image_data(self, image_hash):
        cursor = self.conn.cursor()
        cursor.execute("SELECT image_data FROM images WHERE image_hash = ?", (image_hash,))
        row = cursor.fetchone()
        if row:
            return self.decrypt_data(row[0])
        else:
            print(f"Ошибка: Изображение не найдено в базе данных.")
            return None

    def get_image_hashes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT image_hash FROM images")
        rows = cursor.fetchall()
        if rows:
            return [row[0] for row in rows]
        else:
            return []

    def remove_image(self, image_hash):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM images WHERE image_hash = ?", (image_hash,))
        self.conn.commit()
        print(f"Изображение удалено из базы данных.")

    def encrypt_data(self, data):
        cipher = Fernet(self.key)
        return cipher.encrypt(data)

    def decrypt_data(self, encrypted_data):
        cipher = Fernet(self.key)
        return cipher.decrypt(encrypted_data)

    def backup_database(self, backup_file):
        self.conn.close()
        with open(self.db_name, 'rb') as f_src:
            with open(backup_file, 'wb') as f_dest:
                f_dest.write(f_src.read())
        self.conn = sqlite3.connect(self.db_name)

    def __del__(self):
        self.conn.close()


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

# image_manager = ImageManager()
# image_manager.add_image(r'C:\Users\Ya\Pictures\qwe.png')

# project_builder = ProjectBuilder(image_manager, "VisualNovel")

# image_ids = image_manager.get_image_ids()
# print("Список идентификаторов изображений:", image_ids)

# project_builder.build_project("f34d0c8dac18b6219b2cf382314f5a158937cfa7b785ab9cc1e989d62d7a0757")

