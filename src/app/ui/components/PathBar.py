import flet as ft

from app.ui.components.PathBarButtons import PathBarButtons
from app.ui.components.PathBarDisplay import PathBarDisplay


class PathBar(ft.Container):
    def __init__(self, path: list[str]) -> None:
        super().__init__()

        self.content = ft.Row(
            [
                PathBarButtons(path),
                ft.VerticalDivider(),
                PathBarDisplay(path),
            ],
        )
