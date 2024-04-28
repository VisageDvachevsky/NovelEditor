import pytest

from app.crypto_fs.CryptoFs import CryptoFs


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


def test_delete_non_existent_dir(cfs):
    cfs.remove(["test_folder", "test.txt"])
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is None


def test_delete_non_existent_file(cfs):
    cfs.read_dir(["test_folder"], mkdir=True)
    cfs.remove(["test_folder", "test.txt"])
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is None


def test_open_dir_as_file(cfs):
    cfs.read_dir(["test_folder"], mkdir=True)
    file = cfs.read_file(["test_folder"])
    assert file is None


def test_open_file_as_dir(cfs):
    test_message = "Test message"
    cfs.write_file(["test_folder", "test.txt"], test_message.encode())
    dir = cfs.read_dir(["test_folder", "test.txt"])
    assert dir is None


def test_write_file_in_file(cfs):
    test_message = "Test message"
    cfs.write_file(["test_folder", "test"], test_message.encode())
    cfs.write_file(["test_folder", "test", "text.txt"], test_message.encode())
    file = cfs.read_file(["test_folder", "test", "text.txt"])
    assert file is None


def test_overwrite_existing_file(cfs):
    test_message_1 = "Test message 1"
    cfs.write_file(["test_folder", "test.txt"], test_message_1.encode())
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is not None
    assert file.decode() == test_message_1

    test_message_2 = "Test message 2"
    cfs.write_file(["test_folder", "test.txt"], test_message_2.encode())
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is not None
    assert file.decode() == test_message_2


def test_forbid_overwrite_existing_file(cfs):
    test_message_1 = "Test message 1"
    cfs.write_file(["test_folder", "test.txt"], test_message_1.encode())
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is not None
    assert file.decode() == test_message_1

    test_message_2 = "Test message 2"
    cfs.write_file(
        ["test_folder", "test.txt"], test_message_2.encode(), overwrite=False
    )
    file = cfs.read_file(["test_folder", "test.txt"])
    assert file is not None
    assert file.decode() != test_message_2
    assert file.decode() == test_message_1
