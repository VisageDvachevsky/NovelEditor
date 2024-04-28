from app.crypto_fs.AES import AES
from app.crypto_fs.utility import uuid, as_str, random_key


def test_is_uuid_int():
    uid = uuid()
    assert isinstance(uid, int)


def test_str_uuid_is_safe_path(uid):
    sid = as_str(uid)
    assert " " not in sid
    assert "/" not in sid


def test_str_uuid_is_immutable(uid):
    sid1 = as_str(uid)
    sid2 = as_str(uid)
    assert sid1 == sid2


def test_random_key_is_random():
    key1 = random_key()
    key2 = random_key()
    assert key1 != key2


def test_random_key_correct_length():
    key = random_key()
    assert len(key) == AES.key_size
