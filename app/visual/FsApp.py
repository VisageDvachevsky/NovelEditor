from tkinter import ttk

from app.crypto_fs.CryptoFs import CryptoFs
from app.crypto_fs.load_root import load_root


class FsApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Управление файлами")

        self.fs = CryptoFs("data", load_root("key.key"))

        self.tree = ttk.Treeview(self.master)
        self.tree.pack(fill="both", expand=True)

        self.populate_tree([])

    def populate_tree(self, path: list[str], parent=""):
        files = self.fs.read_dir(path)
        for file_path, file_obj in files.items():
            node = self.tree.insert(parent, "end", text=file_path, open=False)
            if file_obj.type == "dir":
                self.populate_tree(path + [file_path], node)
