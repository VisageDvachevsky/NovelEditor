import pytest

from dataclasses import dataclass
from tkinter import Tk, filedialog


@pytest.fixture
def root():
    return Tk()


@dataclass
class DidCall:
    did_call: bool

    def call(self, *_, **__):
        self.did_call = True


@pytest.fixture
def mock_mainloop(monkeypatch):
    data = DidCall(did_call=False)
    monkeypatch.setattr(Tk, "mainloop", data.call)
    yield data


@pytest.fixture
def mock_filedialog(monkeypatch, tmp_image):
    def my_askopenfilename(*_, **__):
        return tmp_image

    monkeypatch.setattr(filedialog, "askopenfilename", my_askopenfilename)
    yield tmp_image
