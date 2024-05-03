from typing import Callable, Any

import flet as ft


class PathBar(ft.Container):
    def __init__(
        self,
        path: list[str],
        on_path_change: Callable[[list[str]], None] | None = None,
        on_upward: Callable[[Any], None] | None = None,
    ) -> None:
        super().__init__()

        self._on_path_change = on_path_change
        self._path_preview = ft.Row([], wrap=True)

        self._is_mounted = False

        self.content = ft.Row(
            [
                ft.Container(
                    ft.IconButton(icon=ft.icons.ARROW_UPWARD, on_click=on_upward)
                ),
                ft.VerticalDivider(),
                ft.Container(self._path_preview, expand=True),
            ],
        )
        self.set_path(path)

    def did_mount(self) -> None:
        self._is_mounted = True

    def did_unmount(self) -> None:
        self._is_mounted = False

    def set_path(self, path: list[str]) -> None:
        self._path_preview.controls.clear()

        def path_change(p: list[str]) -> None:
            if self._on_path_change:
                self._on_path_change(p)

        self._path_preview.controls.append(
            ft.TextButton(text="Root", on_click=lambda _: path_change([]))
        )
        self._path_preview.controls.append(ft.Text("/"))

        for idx, path_part in enumerate(path):

            def on_click(_, v=idx):
                path_change(path[: v + 1])

            self._path_preview.controls.append(
                ft.TextButton(text=path_part, on_click=on_click)
            )

            if idx + 1 != len(path):
                self._path_preview.controls.append(ft.Text("/"))

        if self._is_mounted:
            self.update()
