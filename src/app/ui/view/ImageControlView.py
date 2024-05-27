import flet as ft


class ImageControlView(ft.ResponsiveRow):
    def __init__(self):
        super().__init__()

        self.expand = True
        self.controls = [ft.Column(controls=[ft.Text("ImageControlView")])]
