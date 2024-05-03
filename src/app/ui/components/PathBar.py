import flet as ft
from mopyx import render, action


class PathBar(ft.Container):
    def __init__(
        self,
        path: list[str],
    ) -> None:
        super().__init__()

        self._path_preview = ft.Row([], wrap=True)

        self._path = path

        def on_upward(*_):
            self.set_path(self._path[:-1] if len(self._path) > 0 else [])

        self.content = ft.Row(
            [
                ft.Row([ft.IconButton(icon=ft.icons.ARROW_UPWARD, on_click=on_upward)]),
                ft.VerticalDivider(),
                self._path_preview,
            ],
        )

    def did_mount(self) -> None:
        self._render()

    @action
    def set_path(self, val: list[str]):
        self._path.clear()
        self._path.extend(val)

    @render
    def _render(self):
        self._path_preview.controls.clear()

        self._path_preview.controls.append(
            ft.TextButton(text="Root", on_click=lambda _: self.set_path([]))
        )
        self._path_preview.controls.append(ft.Text("/"))

        for idx, path_part in enumerate(self._path):

            def on_click(_, v=idx):
                self.set_path(self._path[: v + 1])

            self._path_preview.controls.append(
                ft.TextButton(text=path_part, on_click=on_click)
            )

            if idx + 1 != len(self._path):
                self._path_preview.controls.append(ft.Text("/"))

        self.update()
