import flet as ft

from app.utility.functions import set_list


class PathBarButtons(ft.Row):
    def __init__(self, path: list[str]):
        super().__init__()

        self._path = path
        self.controls = [
            ft.IconButton(
                icon=ft.icons.ARROW_UPWARD,
                on_click=lambda _: set_list(
                    self._path,
                    self._path[:-1] if len(self._path) > 0 else [],
                ),
            )
        ]
