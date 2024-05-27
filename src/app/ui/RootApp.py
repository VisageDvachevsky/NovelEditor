import flet as ft
from mopyx import model, render

from app.ui.view.FileSystemView import FileSystemView
from app.ui.view.ImageControlView import ImageControlView
from app.ui.view.SceneView import SceneView


class RootApp(ft.Row):
    @model
    class Model:
        def __init__(self) -> None:
            self.selected_index = 2

    def __init__(self) -> None:
        super().__init__()
        self.expand = True

        self._model = self.Model()

        def set_selected_index(index):
            self._model.selected_index = index

        self._rail = ft.NavigationRail(
            selected_index=self._model.selected_index,
            min_width=100,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.IMAGE_OUTLINED,
                    selected_icon=ft.icons.IMAGE,
                    label="Управление Изображениями",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.CAMERA_ROLL_OUTLINED,
                    selected_icon=ft.icons.CAMERA_ROLL,
                    label_content=ft.Text("Сцена"),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.FILE_OPEN_OUTLINED,
                    selected_icon=ft.icons.FILE_OPEN,
                    label_content=ft.Text("Файловая Система"),
                ),
            ],
            on_change=lambda _: set_selected_index(self._rail.selected_index),
        )

        self._views: list[ft.Control] = [
            ImageControlView(),
            SceneView(),
            FileSystemView(),
        ]

        self.controls = [
            self._rail,
            ft.VerticalDivider(),
            self._views[self._model.selected_index],
        ]

    def did_mount(self) -> None:
        self._render()

    @render
    def _render(self) -> None:
        self.controls[-1] = self._views[self._model.selected_index]
        self.update()
