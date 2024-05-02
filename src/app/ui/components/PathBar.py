from typing import Callable

import flet as ft


class PathBar(ft.Container):
    def __init__(
        self,
        path: list[str],
        on_path_change: Callable[[list[str]], None] | None = None,
    ) -> None:
        super().__init__()

        self._path = path
        self._on_path_change = on_path_change
        self._row = ft.Row(controls=[], wrap=True)

        self._is_mounted = False

        self.content = self._row
        self.padding = ft.padding.all(10)

        self._update_path()

    def did_mount(self) -> None:
        self._is_mounted = True

    def did_unmount(self) -> None:
        self._is_mounted = False

    def set_path(self, path: list[str]) -> None:
        self._path = path
        self._update_path()

    def _update_path(self) -> None:
        self._row.controls.clear()

        def path_change(path: list[str]) -> None:
            if self._on_path_change:
                self._on_path_change(path)

        self._row.controls.append(
            ft.TextButton(text="Root", on_click=lambda _: path_change([]))
        )
        self._row.controls.append(ft.Text("/"))

        for idx, path_part in enumerate(self._path):

            def on_click(_, v=idx):
                path_change(self._path[: v + 1])

            self._row.controls.append(ft.TextButton(text=path_part, on_click=on_click))

            if idx + 1 != len(self._path):
                self._row.controls.append(ft.Text("/"))

        if self._is_mounted:
            self.update()
