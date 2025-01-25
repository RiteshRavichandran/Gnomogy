# src/gnomoji/main.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gnomoji.ui.main_window import MainWindow  # Use absolute import
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def main():
    # Create the main application window
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
