import flet as ft

from app.ui.RootApp import RootApp


def main(page: ft.Page):
    page.add(RootApp())


if __name__ == "__main__":
    ft.app(main)
