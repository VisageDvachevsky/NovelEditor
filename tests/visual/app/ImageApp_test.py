from app.visual.app.ImageApp import ImageApp


def test_image_app_title():
    assert ImageApp.title()


def test_image_app_add_image(root, mock_filedialog):
    image_app = ImageApp(root)

    image_app.id_entry.delete(0, "end")
    image_app.id_entry.insert(0, "test_id")

    image_app.browse_image()
    assert image_app.add_image()
    assert image_app.image_manager.get_image_data("test_id")


def test_image_app_add_image_no_id(root, mock_filedialog):
    image_app = ImageApp(root)

    image_app.id_entry.delete(0, "end")

    image_app.browse_image()
    assert not image_app.add_image()
    assert image_app.image_manager.get_image_data("test_id") is None


def test_image_app_add_image_no_selection(root, mock_filedialog):
    image_app = ImageApp(root)

    image_app.id_entry.delete(0, "end")
    image_app.id_entry.insert(0, "test_id")

    assert not image_app.add_image()
    assert image_app.image_manager.get_image_data("test_id") is None


def test_image_app_delete_image(root, mock_filedialog):
    image_app = ImageApp(root)

    image_app.id_entry.delete(0, "end")
    image_app.id_entry.insert(0, "test_id")

    image_app.browse_image()
    assert image_app.add_image()
    assert image_app.image_manager.get_image_data("test_id")

    assert image_app.delete_image()
    assert image_app.image_manager.get_image_data("test_id") is None


def test_image_app_delete_image_no_id(root, mock_filedialog):
    image_app = ImageApp(root)

    image_app.id_entry.delete(0, "end")
    image_app.id_entry.insert(0, "test_id")

    image_app.browse_image()
    assert image_app.add_image()
    assert image_app.image_manager.get_image_data("test_id")

    image_app.id_entry.delete(0, "end")
    assert not image_app.delete_image()
    assert image_app.image_manager.get_image_data("test_id")
