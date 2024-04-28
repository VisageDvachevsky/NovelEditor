import pytest


@pytest.fixture(autouse=True)
def change_test_dir(tmp_path, monkeypatch):
    tmp_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(tmp_path)
