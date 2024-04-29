import pytest
from Crypto.Random import get_random_bytes
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
    img_path = tmp_path_factory.mktemp("data") / "img.png"
    data = get_random_bytes(100)
    img_path.write_bytes(data)
    return img_path
