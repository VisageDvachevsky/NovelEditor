import pytest

from app.crypto_fs.CryptoFs import CryptoFs
from app.crypto_fs.model.Root import Root


@pytest.fixture
def root():
    return Root()


@pytest.fixture
def cfs(root):
    return CryptoFs("data", root)


def test_non_existent_dir(cfs):
    dir = cfs.read_dir(["non_existent"])
    assert dir is None


def test_mkdir(cfs):
    dir = cfs.read_dir(["mkdir"], mkdir=True)
    assert dir is not None


def test_read_non_existent_file(cfs):
    file = cfs.read_file(["non_existent.txt"])
    assert file is None


def test_write_file(cfs):
    test_message = "Test message"
    cfs.write_file(["test_folder", "test.txt"], test_message.encode())
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is not None
    assert file.decode() == test_message


def test_delete_file(cfs):
    test_message = "Test message"
    cfs.write_file(["test_folder", "test.txt"], test_message.encode())
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is not None

    cfs.remove(["test_folder", "test.txt"])
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is None


def test_delete_folder(cfs):
    test_message = "Test message"
    cfs.write_file(["test_folder", "test.txt"], test_message.encode())
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is not None

    cfs.remove(["test_folder"])
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is None

    dir = cfs.read_dir(["test_folder"])
    assert dir is None
