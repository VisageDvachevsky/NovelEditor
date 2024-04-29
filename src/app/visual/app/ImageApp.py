from tkinter import ttk, filedialog, Tk
from loguru import logger

from app.image_manager.ImageManager import ImageManager
from app.visual.app.BaseApp import BaseApp


class ImageApp(BaseApp):
    @staticmethod
    def title() -> str:
        return "Управление изображениями"

    def __init__(self, master: Tk = None, **kwargs: dict):
        super().__init__(master, **kwargs)

        self.selected_image_path = None
        self.image_manager = ImageManager()

        self.label = ttk.Label(self, text="Введите ID изображения:")
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.id_entry = ttk.Entry(self)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        self.browse_button = ttk.Button(
            self, text="Выбрать изображение", command=self.browse_image
        )
        self.browse_button.grid(
            row=1, column=0, columnspan=2, padx=10, pady=5, sticky="we"
        )

        self.add_button = ttk.Button(
            self, text="Добавить изображение", command=self.add_image
        )
        self.add_button.grid(
            row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we"
        )

        self.delete_button = ttk.Button(
            self, text="Удалить изображение", command=self.delete_image
        )
        self.delete_button.grid(
            row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we"
        )

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if file_path:
            self.selected_image_path = file_path

    def add_image(self):
        image_id = self.id_entry.get()
        if image_id:
            if hasattr(self, "selected_image_path") and self.selected_image_path:
                self.image_manager.add_image(self.selected_image_path, image_id)
                logger.info(f"Изображение с ID {image_id} добавлено.")
            else:
                logger.error("Выберите изображение.")
        else:
            logger.error("Введите ID изображения.")

    def delete_image(self):
        image_id = self.id_entry.get()
        if image_id:
            self.image_manager.remove_image(image_id)
            logger.info(f"Изображение с ID {image_id} удалено.")
        else:
            logger.error("Введите ID изображения.")
