import hashlib
from tkinter import ttk, filedialog

from app.image_manager.ImageManager import ImageManager


class ImageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Управление изображениями")

        self.image_manager = ImageManager()

        self.label = ttk.Label(self.master, text="Введите ID изображения:")
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.id_entry = ttk.Entry(self.master)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        self.browse_button = ttk.Button(
            self.master, text="Выбрать изображение", command=self.browse_image
        )
        self.browse_button.grid(
            row=1, column=0, columnspan=2, padx=10, pady=5, sticky="we"
        )

        self.add_button = ttk.Button(
            self.master, text="Добавить изображение", command=self.add_image
        )
        self.add_button.grid(
            row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we"
        )

        self.delete_button = ttk.Button(
            self.master, text="Удалить изображение", command=self.delete_image
        )
        self.delete_button.grid(
            row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we"
        )

        self.backup_button = ttk.Button(
            self.master, text="Создать резервную копию", command=self.backup_database
        )
        self.backup_button.grid(
            row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we"
        )

        for child in self.master.winfo_children():
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
                hashed_id = hashlib.sha256(image_id.encode()).hexdigest()
                self.image_manager.add_image(self.selected_image_path, hashed_id)
                print(f"Изображение с ID {image_id} добавлено.")
            else:
                print("Ошибка: Выберите изображение.")
        else:
            print("Ошибка: Введите ID изображения.")

    def delete_image(self):
        image_id = self.id_entry.get()
        if image_id:
            hashed_id = hashlib.sha256(image_id.encode()).hexdigest()
            self.image_manager.remove_image(hashed_id)
            print(f"Изображение с ID {image_id} удалено.")
        else:
            print("Ошибка: Введите ID изображения.")

    def backup_database(self):
        self.image_manager.backup_database("backup.db")
        print("Создана резервная копия базы данных.")
