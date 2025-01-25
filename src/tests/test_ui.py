# src/tests/test_ui.py
import pytest
from gnomoji.ui.main_window import MainWindow
from gi.repository import Gtk


@pytest.fixture
def main_window():
    """Fixture to create a MainWindow instance for testing."""
    return MainWindow()


def test_main_window_initialization(main_window):
    """Test that the MainWindow initializes correctly."""
    assert main_window.get_title() == "Gnomoji"
    assert isinstance(main_window.search_entry, Gtk.SearchEntry)
    assert isinstance(main_window.flow_box, Gtk.FlowBox)


def test_load_all_emojis(main_window):
    """Test that all emojis are loaded into the flow box."""
    main_window.load_all_emojis()
    children = main_window.flow_box.get_children()
    assert len(children) > 0  # Ensure emojis are loaded
    # Access the button inside the FlowBoxChild
    button = children[0].get_child()
    assert isinstance(button, Gtk.Button)  # Ensure children are buttons


def test_load_top_matches(main_window):
    """Test that the top matches are loaded into the flow box."""
    test_matches = ["😊", "😄", "😁"]
    main_window.load_top_matches(test_matches)
    children = main_window.flow_box.get_children()
    assert len(children) == len(
        test_matches
    )  # Ensure correct number of matches are loaded
    for child, emoji_char in zip(children, test_matches):
        # Access the button inside the FlowBoxChild
        button = child.get_child()
        assert (
            button.get_label() == emoji_char
        )  # Ensure buttons have the correct labels


def test_clear_flow_box(main_window):
    """Test that the flow box is cleared correctly."""
    main_window.load_all_emojis()
    assert len(main_window.flow_box.get_children()) > 0  # Ensure emojis are loaded
    main_window.clear_flow_box()
    assert len(main_window.flow_box.get_children()) == 0  # Ensure flow box is cleared


def test_on_search_changed(main_window):
    """Test that the search functionality updates the flow box."""
    # Simulate a search query
    main_window.search_entry.set_text("smil")
    main_window.on_search_changed(main_window.search_entry)
    children = main_window.flow_box.get_children()
    assert len(children) <= 10  # Ensure only top 10 matches are shown
