from typing import Type

from app.visual.app.BaseApp import BaseApp
from app.visual.app.FsApp import FsApp
from app.visual.app.ImageApp import ImageApp
from app.visual.app.SceneApp import SceneApp


def select_mode(mode: str | None) -> Type[BaseApp] | None:
    match mode:
        case "scene":
            return SceneApp
        case "image_app":
            return ImageApp
        case "fs":
            return FsApp

        case _:
            return None
