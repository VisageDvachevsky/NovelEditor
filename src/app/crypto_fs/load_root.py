import pickle

from pathlib import Path

from app.crypto_fs.AES import AES
from app.crypto_fs.model.Root import Root


def load_root(root_file: str) -> Root:
    path = Path(root_file)

    if path.exists():
        data = path.read_bytes()
        key = data[: AES.key_size]
        uid = pickle.loads(data[AES.key_size :])
        res = Root(uid, key)
    else:
        res = Root()
        path.write_bytes(res.key + pickle.dumps(res.uid))

    return res
