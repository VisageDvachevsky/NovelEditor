from pathlib import Path

import pytest
from Crypto.Random import get_random_bytes

from app.image_manager.ImageManager import ImageManager


@pytest.fixture
def im():
    return ImageManager("data", "key")


def test_image_manager_add_get(im, tmp_image):
    add = im.add_image(tmp_image, "hash")
    assert add

    out = im.get_image_data("hash")
    assert out is not None
    assert out == tmp_image.read_bytes()


def test_image_manager_add_non_existent(im):
    path = Path("this/path/does/not/exist")
    assert not path.exists()

    res = im.add_image(path, "hash")
    assert not res


def test_image_manager_get_non_existent(im):
    data = im.get_image_data("this_hash_does_not_exist")
    assert data is None


def test_remove_image(im, tmp_image):
    im.add_image(tmp_image, "hash")
    data = im.get_image_data("hash")
    assert data is not None

    im.remove_image("hash")
    data = im.get_image_data("hash")
    assert data is None
