import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import hashlib
import os
from io import BytesIO
import Image_Manager

class SceneApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Сцена с изображением")

        self.image_manager = Image_Manager.ImageManager()  

        self.canvas = tk.Canvas(self.master, width=400, height=300)
        self.canvas.pack(pady=10)

        self.load_button = ttk.Button(self.master, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack(pady=5)

        self.id_label = ttk.Label(self.master, text="Введите ID изображения:")
        self.id_label.pack()

        self.id_entry = ttk.Entry(self.master)
        self.id_entry.pack()

    def load_image(self):
        image_id = self.id_entry.get()
        if image_id:
            hashed_id = hashlib.sha256(image_id.encode()).hexdigest()
            image_data = self.image_manager.get_image_data(hashed_id)
            if image_data:
                image = Image.open(BytesIO(image_data))
                photo = ImageTk.PhotoImage(image)

                self.canvas.create_image(200, 150, image=photo)
                self.canvas.image = photo 

                print("Изображение загружено успешно.")
            else:
                print("Ошибка: Изображение с указанным ID не найдено.")
        else:
            print("Ошибка: Введите ID изображения.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SceneApp(root)
    root.mainloop()
