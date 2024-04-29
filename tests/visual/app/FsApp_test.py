from tkinter import ttk
from itertools import chain

from app.crypto_fs.CryptoFs import CryptoFs
from app.crypto_fs.load_root import load_root
from app.visual.app.FsApp import FsApp


def extract_children(
    tree: ttk.Treeview, item: str | int | None = None, prefix: list[str] | None = None
) -> list[list[str]]:
    item_ids = tree.get_children(item)
    prefix = prefix if prefix is not None else []
    if len(item_ids) == 0:
        return [prefix]

    return list(
        chain.from_iterable(
            extract_children(tree, item_id, prefix + [tree.item(item_id, "text")])
            for item_id in item_ids
        )
    )


def test_fs_app_title():
    assert FsApp.title()


def test_fs_app(root):
    file_structure = [
        ["a", "b", "c", "file"],
        ["a", "b", "file"],
        ["a", "file"],
        ["file"],
    ]

    cfs = CryptoFs("data", load_root("key.key"))
    for file in file_structure:
        cfs.write_file(file, "Test Data".encode())

    fs_app = FsApp(root)
    children = extract_children(fs_app.tree)

    # TODO: order?
    assert file_structure == children
