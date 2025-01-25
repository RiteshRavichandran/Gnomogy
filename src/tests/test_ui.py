# src/tests/test_ui.py
import pytest
from gnomoji.ui.main_window import MainWindow


def test_main_window_initialization():
    win = MainWindow()
    assert win.get_title() == "Gnomoji"
