# src/tests/test_utils.py
from gnomoji.utils.emoji_data import load_emojis


def test_load_emojis():
    emojis = load_emojis()
    assert isinstance(emojis, dict)
    assert len(emojis) > 0
