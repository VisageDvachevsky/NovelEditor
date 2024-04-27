import sys
import tkinter as tk

from app.Screne import SceneApp
from app.ImageApp import ImageApp


def main(args: list[str]) -> None:
    if len(args) < 2:
        print("Не указан режим выполнения")

    match args[1]:
        case "scene":
            app = SceneApp
        case "image_app":
            app = ImageApp
        case _:
            print("Неизвестный режим выполнения")
            return

    root = tk.Tk()
    app(root)
    root.mainloop()


if __name__ == "__main__":
    main(sys.argv)
