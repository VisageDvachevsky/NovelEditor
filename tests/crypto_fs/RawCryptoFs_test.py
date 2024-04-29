from pathlib import Path

import pytest
from Crypto.Random import get_random_bytes

from app.crypto_fs.RawCryptoFs import RawCryptoFs
from app.crypto_fs.utility import random_key


@pytest.fixture
def rcf():
    return RawCryptoFs("data")


def test_creates_data_folder():
    RawCryptoFs("data_folder")
    path = Path("data_folder")
    assert path.exists()
    assert path.is_dir()


def test_read_write_bytes(rcf, uid, key):
    data = get_random_bytes(100)
    rcf.write_bytes(uid, key, data)
    out = rcf.read_bytes(uid, key)
    assert out is not None
    assert out == data


def test_read_write_pickle(rcf, uid, key):
    test = ["this", "is", {"test": "object"}, 42]
    rcf.write_pickle(uid, key, test)
    out = rcf.read_pickle(uid, key)

    assert out is not None
    # TODO: This passes the test for some reason, but I'm not sure
    #       if it is a correct way to compare these objects
    assert out == test


def test_remove(rcf, uid, key):
    rcf.write_bytes(uid, key, get_random_bytes(100))
    out = rcf.read_bytes(uid, key)
    assert out is not None

    rcf.remove(uid)
    out = rcf.read_bytes(uid, key)
    assert out is None


def test_read_bytes_non_existent(rcf, uid, key):
    out = rcf.read_bytes(uid, key)
    assert out is None


def test_read_pickle_non_existent(rcf, uid, key):
    out = rcf.read_pickle(uid, key)
    assert out is None


def test_read_invalid_pickle(rcf, uid, key):
    rcf.write_bytes(uid, key, get_random_bytes(100))
    out = rcf.read_pickle(uid, key)
    assert out is None


def test_read_undecryptable_bytes(rcf, uid, key):
    rcf.write_bytes(uid, key, get_random_bytes(100))
    out = rcf.read_bytes(uid, random_key())
    assert out is None


def test_read_undecryptable_pickle(rcf, uid, key):
    rcf.write_pickle(uid, key, ["test", {"test": "object"}])
    out = rcf.read_pickle(uid, random_key())
    assert out is None


def test_remove_non_existent(rcf, uid, key):
    rcf.remove(uid)
