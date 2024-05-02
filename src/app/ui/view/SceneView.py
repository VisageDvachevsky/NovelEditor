import flet as ft


class SceneView(ft.ResponsiveRow):
    def __init__(self):
        super().__init__()

        self.expand = True
        self.controls = [ft.Column(controls=[ft.Text("SceneView")])]
