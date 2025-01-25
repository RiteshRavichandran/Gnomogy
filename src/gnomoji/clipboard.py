# src/gnomoji/clipboard.py
import pyperclip


def copy_to_clipboard(text):
    """Copy the given text to the clipboard."""
    pyperclip.copy(text)
