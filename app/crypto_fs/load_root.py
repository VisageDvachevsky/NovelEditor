import os
import pickle


from app.crypto_fs.CryptoFs import CryptoFs
from app.crypto_fs.model.Root import Root


def load_root(root_file: str) -> Root:
    if os.path.exists(root_file):
        with open(root_file, "rb") as f:
            return pickle.load(f)

    root = Root(uid=CryptoFs.uuid(), key=CryptoFs.random_key())
    with open(root_file, "wb") as f:
        pickle.dump(root, f)
    return root
