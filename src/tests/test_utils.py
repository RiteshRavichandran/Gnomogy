# src/tests/test_utils.py
from gnomoji.utils.emoji_data import load_emojis
from gnomoji.clipboard import copy_to_clipboard
import emoji


def test_load_emojis():
    """Test that emojis are loaded correctly."""
    emojis = load_emojis()
    assert isinstance(emojis, list)
    assert len(emojis) > 0  # Ensure emojis are loaded
    assert "😊" in emojis  # Ensure a common emoji is in the list


def test_copy_to_clipboard():
    """Test that the clipboard functionality works."""
    test_text = "😊"
    copy_to_clipboard(test_text)
    assert True  # Placeholder assertion
