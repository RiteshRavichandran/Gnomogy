# src/gnomoji/ui/main_window.py
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gnomoji")
        self.set_default_size(400, 300)

        # Create a grid to hold emojis
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # Add a search bar
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search emojis...")
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.grid.attach(self.search_entry, 0, 0, 5, 1)  # Place at the top

        # Load emojis
        self.load_emojis()

    def load_emojis(self):
        # Placeholder for emoji loading
        for i in range(20):  # Example: Add 20 placeholder buttons
            button = Gtk.Button(label="😊")
            self.grid.attach(
                button, i % 5, i // 5 + 1, 1, 1
            )  # Arrange in a 5-column grid

    def on_search_changed(self, entry):
        # Placeholder for search functionality
        query = entry.get_text().lower()
        print(f"Search query: {query}")
