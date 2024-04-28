import pickle

from pathlib import Path
from Crypto.Random import get_random_bytes

from app.crypto_fs.AES import AES
from app.crypto_fs.CryptoFs import CryptoFs
from app.crypto_fs.model.Root import Root


def load_root(root_file: str) -> Root:
    path = Path(root_file)

    if path.exists():
        data = path.read_bytes()
        key = data[: AES.key_size]
        uid = pickle.loads(data[AES.key_size :])
    else:
        key = get_random_bytes(AES.key_size)
        uid = CryptoFs.uuid()
        path.write_bytes(key + pickle.dumps(uid))

    return Root(uid, key)
