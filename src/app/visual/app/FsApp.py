from tkinter import ttk, Tk

from app.crypto_fs.CryptoFs import CryptoFs
from app.crypto_fs.load_root import load_root
from app.visual.app.BaseApp import BaseApp


class FsApp(BaseApp):
    @staticmethod
    def title() -> str:
        return "Управление файлами"

    def __init__(self, master: Tk = None, **kwargs: dict):
        super().__init__(master, **kwargs)

        self.fs = CryptoFs("data", load_root("key.key"))

        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True)

        self.populate_tree([])

    def populate_tree(self, path: list[str], parent=""):
        files = self.fs.read_dir(path)
        for file_path, file_obj in files.items():
            node = self.tree.insert(parent, "end", text=file_path, open=False)
            if file_obj.type == "dir":
                self.populate_tree(path + [file_path], node)
