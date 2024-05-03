import flet as ft
from mopyx import action, render

from app.crypto_fs.CryptoFs import CryptoFs


class FsPreview(ft.Row):
    def __init__(self, fs: CryptoFs, path: list[str]):
        super().__init__()

        self._fs = fs
        self._path = path

        self.spacing = 10
        self.wrap = True

    def did_mount(self) -> None:
        self._render()

    @action
    def set_path(self, val: list[str]):
        self._path.clear()
        self._path.extend(val)

    @render
    def _render(self):
        self.controls.clear()

        folder = self._fs.read_dir(path=self._path)
        if folder is not None:

            for name, item in folder.items():

                def on_click(_, n=name, i=item) -> None:
                    if i.type == "dir":
                        self.set_path(self._path + [n])

                self.controls.append(
                    ft.TextButton(
                        icon=(
                            ft.icons.FOLDER
                            if item.type == "dir"
                            else ft.icons.FILE_PRESENT
                        ),
                        text=name,
                        on_click=on_click,
                    )
                )

        self.update()
