from pathlib import Path

import flet as ft

from app.ui.RootApp import RootApp


def main(page: ft.Page):
    page.add(RootApp())


if __name__ == "__main__":
    assets_dir = Path(Path(__file__).parent, "assets")
    ft.app(main, assets_dir=assets_dir)
