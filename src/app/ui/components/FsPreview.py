from typing import Callable

import flet as ft

from app.crypto_fs.CryptoFs import CryptoFs


class FsPreview(ft.Row):
    def __init__(
        self,
        fs: CryptoFs,
        path: list[str],
        on_path_change: Callable[[list[str]], None] | None = None,
    ):
        super().__init__()

        self._fs = fs
        self._path = path
        self._on_path_change = on_path_change

        self._is_mounted = False

        self._update_path()

        self.spacing = 10
        self.wrap = True

    def did_mount(self) -> None:
        self._is_mounted = True

    def did_umount(self) -> None:
        self._is_mounted = False

    def set_path(self, path: list[str]) -> None:
        self._path = path
        self._update_path()

    def _update_path(self):
        self.controls.clear()

        dir = self._fs.read_dir(path=self._path)
        if dir is not None:

            def path_change(path: list[str]) -> None:
                if self._on_path_change:
                    self._on_path_change(path)

            for name, item in dir.items():

                def on_click(_, n=name, i=item) -> None:
                    if i.type == "dir":
                        path_change(self._path + [n])

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

        if self._is_mounted:
            self.update()
