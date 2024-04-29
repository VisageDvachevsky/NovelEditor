import tkinter as tk
from abc import ABC, abstractmethod


class BaseApp(tk.Frame, ABC):
    @staticmethod
    @abstractmethod
    def title() -> str:
        raise NotImplementedError

    @abstractmethod
    def __init__(self, master: tk.Tk = None, **kwargs: dict):
        super().__init__(master, **kwargs)
