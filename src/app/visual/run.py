import tkinter as tk

from typing import Type
from loguru import logger

from app.visual.app.BaseApp import BaseApp
from app.visual.select_mode import select_mode


def run(mode: str | None) -> None:
    app: Type[BaseApp] = select_mode(mode)
    if app is None:
        logger.error(f"Неизвестный режим выполнения '{mode}'")
        return

    root = tk.Tk()
    root.title(app.title())
    app(root).pack(fill="both", expand=True)
    root.mainloop()
