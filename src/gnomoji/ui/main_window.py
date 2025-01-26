# src/gnomoji/ui/main_window.py
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from gnomoji.utils.emoji_data import load_emojis
from gnomoji.clipboard import copy_to_clipboard
from fuzzywuzzy import process
import emoji
from threading import Thread
import warnings


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
        self.emoji_descriptions = [
            emoji.EMOJI_DATA[char]["en"] for char in self.emojis
        ]  # Precompute descriptions
        self.current_page = 0  # Track the current page for pagination
        self.load_page()  # Load the first page of emojis

        # Cache for search results
        self.search_cache = {}

    def load_page(self):
        """Load a page of emojis (50 at a time)."""
        start = self.current_page * 50
        end = start + 50
        for emoji_char in self.emojis[start:end]:
            button = Gtk.Button(label=emoji_char)
            button.connect("clicked", self.on_emoji_clicked, emoji_char)
            self.flow_box.add(button)
        self.flow_box.show_all()
        self.current_page += 1

    def clear_flow_box(self):
        """Remove all children from the flow box."""
        for child in self.flow_box.get_children():
            self.flow_box.remove(child)

    def on_emoji_clicked(self, button, emoji_char):
        """Handle emoji button clicks."""
        print(f"Attempting to copy {emoji_char} to clipboard...")
        copy_to_clipboard(emoji_char)

    def on_search_changed(self, entry):
        """Filter emojis based on the search query using fuzzy search."""
        query = entry.get_text().lower()

        # Sanitize the query to remove non-text characters (e.g., emojis)
        sanitized_query = "".join(
            char for char in query if char.isalnum() or char.isspace()
        )

        # Update the search bar text if it was sanitized
        if sanitized_query != query:
            entry.set_text(sanitized_query)
            entry.set_position(-1)  # Move the cursor to the end

        # Handle empty query
        if not sanitized_query:
            self.clear_flow_box()
            self.current_page = 0
            self.load_page()  # Reload the first page of emojis
            return

        # Perform fuzzy search in a background thread
        Thread(target=self.perform_search, args=(sanitized_query,), daemon=True).start()

    def perform_search(self, query):
        """Perform fuzzy search and update the UI with the results."""
        if query in self.search_cache:
            matched_emojis = self.search_cache[query]
        else:
            # Suppress fuzzywuzzy warning for empty query
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # Find the top 10 closest matches using fuzzywuzzy
                matches = process.extract(query, self.emoji_descriptions, limit=10)
                matched_emojis = [
                    self.emojis[self.emoji_descriptions.index(desc)]
                    for desc, score in matches
                    if score > 50
                ]
                self.search_cache[query] = matched_emojis  # Cache the results

        # Update the UI in the main thread
        GLib.idle_add(self.update_flow_box, matched_emojis)

    def update_flow_box(self, matched_emojis):
        """Update the flow box with the matched emojis."""
        self.clear_flow_box()
        for emoji_char in matched_emojis:
            button = Gtk.Button(label=emoji_char)
            button.connect("clicked", self.on_emoji_clicked, emoji_char)
            self.flow_box.add(button)
        self.flow_box.show_all()

    def on_scroll(self, widget, event):
        """Handle scroll events for pagination."""
        adj = self.scrolled_window.get_vadjustment()
        if adj.get_upper() - adj.get_page_size() <= adj.get_value():
            self.load_page()  # Load the next page when scrolling to the bottom
