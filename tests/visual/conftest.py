import pytest

from dataclasses import dataclass
from tkinter import Tk, filedialog


@pytest.fixture
def root():
    return Tk()


@pytest.fixture
def mock_filedialog(monkeypatch, tmp_image):
    def my_askopenfilename(*_, **__):
        return tmp_image

    monkeypatch.setattr(filedialog, "askopenfilename", my_askopenfilename)
    yield tmp_image
