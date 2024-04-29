from tkinter import Canvas

import pytest

from app.visual.app.SceneApp import SceneApp


# TODO: Ugly fix
@pytest.fixture(autouse=True)
def mock_canvas_create_image(monkeypatch):
    def dummy(*_, **__):
        pass

    monkeypatch.setattr(Canvas, "create_image", dummy)


def test_scene_app_title():
    assert SceneApp.title()


def test_scene_app_load_image(root, tmp_image):
    scene_app = SceneApp(root)

    scene_app.image_manager.add_image(tmp_image, "test_image")

    scene_app.id_entry.delete(0, "end")
    scene_app.id_entry.insert(0, "test_image")

    assert scene_app.load_image()


def test_scene_app_load_image_no_id(root, tmp_image):
    scene_app = SceneApp(root)

    scene_app.image_manager.add_image(tmp_image, "test_image")

    assert not scene_app.load_image()


def test_scene_app_load_image_no_image(root):
    scene_app = SceneApp(root)

    scene_app.id_entry.delete(0, "end")
    scene_app.id_entry.insert(0, "test_image")

    assert not scene_app.load_image()
