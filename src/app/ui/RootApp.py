import flet as ft

from app.ui.view.FileSystemView import FileSystemView
from app.ui.view.ImageControlView import ImageControlView
from app.ui.view.SceneView import SceneView


class RootApp(ft.UserControl):
    def __init__(self):
        super().__init__(expand=True)

        self._selected_view: ft.Control = ImageControlView(expand=True)
        self._row: ft.Row | None = None

    def set_index(self, index: int) -> None:
        match index:
            case 0:
                self._selected_view = ImageControlView(expand=True)
            case 1:
                self._selected_view = SceneView(expand=True)
            case 2:
                self._selected_view = FileSystemView(expand=True)
            case _:
                self._selected_view = ft.Text("Unknown index")

        self._row.controls[-1] = self._selected_view
        self.update()

    def build(self):

        rail = ft.NavigationRail(
            selected_index=0,
            min_width=100,
            destinations=[
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.IMAGE_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.IMAGE),
                    label="Управление Изображениями",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.CAMERA_ROLL_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.CAMERA_ROLL),
                    label_content=ft.Text("Сцена"),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.FILE_OPEN_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.FILE_OPEN),
                    label_content=ft.Text("Файловая Система"),
                ),
            ],
            on_change=lambda e: self.set_index(e.control.selected_index),
        )

        self._row = ft.Row(
            [rail, ft.VerticalDivider(width=1), self._selected_view],
            expand=True,
        )

        return self._row
