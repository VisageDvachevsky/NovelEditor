import flet as ft
from mopyx import render

from app.crypto_fs.CryptoFs import CryptoFs
from app.utility.functions import set_list


class FsPreview(ft.Row):
    def __init__(self, fs: CryptoFs, path: list[str]):
        super().__init__()

        self.spacing = 10
        self.wrap = True

        self._fs = fs
        self._path = path

    def did_mount(self) -> None:
        self._render()

    @render
    def _render(self):
        self.controls.clear()

        folder = self._fs.read_dir(path=self._path)
        if folder is not None:

            for name, item in folder.items():

                def on_click(_, n=name, i=item) -> None:
                    if i.type == "dir":
                        set_list(self._path, self._path + [n])

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
