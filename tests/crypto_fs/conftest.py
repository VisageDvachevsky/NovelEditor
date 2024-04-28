import pytest

from app.crypto_fs.model.Root import Root
from app.crypto_fs.utility import random_key, uuid


@pytest.fixture
def key():
    return random_key()


@pytest.fixture
def uid():
    return uuid()


@pytest.fixture
def root():
    return Root()
