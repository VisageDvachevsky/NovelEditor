import flet as ft
from mopyx import render, model, action

from app.crypto_fs.CryptoFs import CryptoFs
from app.crypto_fs.load_root import load_root
from app.ui.components.FsPreview import FsPreview
from app.ui.components.PathBar import PathBar


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

        @action
        def on_path_change(path: list[str]) -> None:
            self._model.path.clear()
            self._model.path.extend(path)

        def on_upward(*_):
            on_path_change(self._model.path[:-1] if len(self._model.path) > 0 else [])

        self._path_bar = PathBar(
            path=self._model.path, on_path_change=on_path_change, on_upward=on_upward
        )
        self._fs_preview = FsPreview(
            fs=self.fs, path=self._model.path, on_path_change=on_path_change
        )
        self.controls = [self._path_bar, ft.Divider(), self._fs_preview]

    def did_mount(self) -> None:
        self._render()

    @render
    def _render(self) -> None:
        self._render_path_bar()
        self._render_fs_preview()

    @render(ignore_updates=True)
    def _render_path_bar(self) -> None:
        self._path_bar.set_path(self._model.path)

    @render(ignore_updates=True)
    def _render_fs_preview(self) -> None:
        self._fs_preview.set_path(self._model.path)
