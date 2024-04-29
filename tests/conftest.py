from dataclasses import dataclass
from tkinter import Tk

import pytest
from _pytest.logging import LogCaptureFixture
from loguru import logger


@pytest.fixture(autouse=True)
def change_test_dir(tmp_path, monkeypatch):
    tmp_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,
    )
    yield caplog
    logger.remove(handler_id)


@pytest.fixture
def reportlog(pytestconfig):
    logging_plugin = pytestconfig.pluginmanager.getplugin("logging-plugin")
    handler_id = logger.add(logging_plugin.report_handler, format="{message}")
    yield
    logger.remove(handler_id)


@pytest.fixture
def tmp_image(tmp_path_factory):
    img_path = tmp_path_factory.mktemp("data") / "img.bmp"
    data = bytes(
        [
            0x42,
            0x4D,
            0x1E,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x1A,
            0x00,
            0x00,
            0x00,
            0x0C,
            0x00,
            0x00,
            0x00,
            0x01,
            0x00,
            0x01,
            0x00,
            0x01,
            0x00,
            0x18,
            0x00,
            0x00,
            0x00,
            0xFF,
            0x00,
        ]
    )
    img_path.write_bytes(data)
    return img_path


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
