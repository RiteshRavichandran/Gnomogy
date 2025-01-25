# src/gnomoji/ui/main_window.py
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gnomoji.utils.emoji_data import load_emojis
from gnomoji.clipboard import copy_to_clipboard


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gnomoji")
        self.set_default_size(400, 300)

        # Create a vertical box to hold the search bar and emoji flow box
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        # Add a search bar
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search emojis...")
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.box.pack_start(self.search_entry, False, False, 0)

        # Add a scrolled window to hold the emoji flow box
        self.scrolled_window = Gtk.ScrolledWindow()
        self.box.pack_start(self.scrolled_window, True, True, 0)

        # Create a flow box to hold emojis
        self.flow_box = Gtk.FlowBox()
        self.scrolled_window.add(self.flow_box)

        # Load emojis
        self.emojis = load_emojis()
        self.load_emojis()

    def load_emojis(self):
        """Populate the flow box with emojis."""
        for emoji_char in self.emojis:
            button = Gtk.Button(label=emoji_char)
            button.connect("clicked", self.on_emoji_clicked, emoji_char)
            self.flow_box.add(button)

    def on_emoji_clicked(self, button, emoji_char):
        """Handle emoji button clicks."""
        print(f"Attempting to copy {emoji_char} to clipboard...")
        copy_to_clipboard(emoji_char)

    def on_search_changed(self, entry):
        """Filter emojis based on the search query."""
        query = entry.get_text().lower()
        for child in self.flow_box.get_children():
            if isinstance(child, Gtk.Button):
                emoji_char = child.get_label()
                if query in emoji_char.lower():  # Case-insensitive search
                    child.show()
                else:
                    child.hide()
