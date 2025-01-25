# src/gnomoji/utils/emoji_data.py
import emoji


def load_emojis():
    """Load and return a list of emoji characters."""
    return list(emoji.EMOJI_DATA.keys())
