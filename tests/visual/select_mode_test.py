from app.visual import select_mode
from app.visual.app.FsApp import FsApp
from app.visual.app.ImageApp import ImageApp
from app.visual.app.SceneApp import SceneApp


def test_select_mode():
    assert select_mode.select_mode("scene") == SceneApp
    assert select_mode.select_mode("image_app") == ImageApp
    assert select_mode.select_mode("fs") == FsApp
    assert select_mode.select_mode(None) is None
