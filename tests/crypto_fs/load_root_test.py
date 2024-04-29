import pickle
from pathlib import Path


from app.crypto_fs.AES import AES
from app.crypto_fs.load_root import load_root
from app.crypto_fs.utility import random_key, uuid


def test_non_existent_file():
    root = load_root("key")
    assert root is not None

    path = Path("key")
    assert path.exists()
    assert path.is_file()

    data = path.read_bytes()
    assert data[: AES.key_size] == root.key
    assert pickle.loads(data[AES.key_size :]) == root.uid


def test_existent_file():
    path = Path("key")
    key = random_key()
    uid = uuid()
    path.write_bytes(key + pickle.dumps(uid))

    root = load_root("key")
    assert key == root.key
    assert uid == root.uid
