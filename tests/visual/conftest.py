from tkinter import Tk

import pytest


@pytest.fixture
def root():
    return Tk()
