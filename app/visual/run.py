from app.visual.ImageApp import ImageApp
from app.visual.SceneApp import SceneApp
import tkinter as tk


def run(mode: str | None) -> None:
    if mode is None:
        print("Не указан режим выполнения")

    match mode:
        case "scene":
            app = SceneApp
        case "image":
            app = ImageApp

        case _:
            print(f"Неизвестный режим выполнения '{mode}'")
            return

    root = tk.Tk()
    app(root)
    root.mainloop()
