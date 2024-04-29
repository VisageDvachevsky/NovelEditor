from dataclasses import dataclass
from tkinter import Tk

import pytest

from app.visual import run


@pytest.fixture
def mock_mainloop(monkeypatch):
    @dataclass
    class MockMainLoopData:
        did_call: bool

        def call(self, *_, **__):
            self.did_call = True

    data = MockMainLoopData(did_call=False)
    monkeypatch.setattr(Tk, "mainloop", data.call)
    yield data


def test_run_known(mock_mainloop):
    run("image_app")
    assert mock_mainloop.did_call


def test_run_unknown(mock_mainloop):
    run(None)
    assert not mock_mainloop.did_call
