import flet as ft
from mopyx import model

from app.crypto_fs.CryptoFs import CryptoFs
from app.crypto_fs.load_root import load_root
from app.ui.components.FsPreview import FsPreview
from app.ui.components.PathBar import PathBar
from app.utility.Proxy import Proxy


class FileSystemView(ft.Column):
    @model
    class Model:
        def __init__(self) -> None:
            self.path = []

    def __init__(self):
        super().__init__()

        self.expand = True

        self.fs = CryptoFs("data", load_root("key.key"))
        self._model = self.Model()

        path_proxy = Proxy(lambda: self._model.path)
        self._path_bar = PathBar(path_proxy)
        self._fs_preview = FsPreview(self.fs, path_proxy)

        self.controls = [self._path_bar, ft.Divider(), self._fs_preview]
