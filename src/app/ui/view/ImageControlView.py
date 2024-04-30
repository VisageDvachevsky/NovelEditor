import flet as ft


class ImageControlView(ft.UserControl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self):
        return ft.Text("ImageControlView")
