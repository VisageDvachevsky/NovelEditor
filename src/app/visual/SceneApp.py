import tkinter as tk

from io import BytesIO
from tkinter import ttk
from PIL import Image, ImageTk
from loguru import logger

from app.image_manager.ImageManager import ImageManager


class SceneApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Сцена с изображением")

        self.image_manager = ImageManager()

        self.canvas = tk.Canvas(self.master, width=400, height=300)
        self.canvas.pack(pady=10)

        self.load_button = ttk.Button(
            self.master, text="Загрузить изображение", command=self.load_image
        )
        self.load_button.pack(pady=5)

        self.id_label = ttk.Label(self.master, text="Введите ID изображения:")
        self.id_label.pack()

        self.id_entry = ttk.Entry(self.master)
        self.id_entry.pack()

    def load_image(self):
        image_id = self.id_entry.get()
        if image_id:
            image_data = self.image_manager.get_image_data(image_id)
            if image_data:
                image = Image.open(BytesIO(image_data))
                photo = ImageTk.PhotoImage(image)

                self.canvas.create_image(200, 150, image=photo)
                self.canvas.image = photo

                logger.info("Изображение загружено успешно.")
            else:
                logger.error("Изображение с указанным ID не найдено.")
        else:
            logger.error("Введите ID изображения.")
