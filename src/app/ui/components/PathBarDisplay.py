import flet as ft
from mopyx import render

from app.utility.functions import set_list


class PathBarDisplay(ft.Row):
    def __init__(self, path: list[str]) -> None:
        super().__init__()

        self.wrap = True
        self._path = path

    def did_mount(self):
        self._render()

    @render
    def _render(self):
        self.controls.clear()

        self.controls.append(
            ft.TextButton(text="Root", on_click=lambda _: set_list(self._path, []))
        )
        self.controls.append(ft.Text("/"))

        for idx, path_part in enumerate(self._path):

            self.controls.append(
                ft.TextButton(
                    text=path_part,
                    on_click=lambda _, v=idx: set_list(self._path, self._path[: v + 1]),
                )
            )

            if idx + 1 != len(self._path):
                self.controls.append(ft.Text("/"))

        self.update()
