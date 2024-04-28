import tkinter as tk

from loguru import logger

from app.visual.FsApp import FsApp
from app.visual.ImageApp import ImageApp
from app.visual.SceneApp import SceneApp


def run(mode: str | None) -> None:
    match mode:
        case "scene":
            app = SceneApp
        case "image_app":
            app = ImageApp
        case "fs":
            app = FsApp

        case _:
            logger.error(f"Неизвестный режим выполнения '{mode}'")
            return

    root = tk.Tk()
    app(root)
    root.mainloop()
