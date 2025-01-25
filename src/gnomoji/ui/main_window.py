# src/gnomoji/ui/main_window.py
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gnomoji.utils.emoji_data import load_emojis
from gnomoji.clipboard import copy_to_clipboard
from fuzzywuzzy import process
import emoji


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
        self.load_all_emojis()  # Load all emojis initially

    def load_all_emojis(self):
        """Populate the flow box with all emojis."""
        self.clear_flow_box()
        for emoji_char in self.emojis:
            button = Gtk.Button(label=emoji_char)
            button.connect("clicked", self.on_emoji_clicked, emoji_char)
            self.flow_box.add(button)
        self.flow_box.show_all()  # Ensure all buttons are visible

    def load_top_matches(self, matches):
        """Populate the flow box with the top 10 matched emojis."""
        self.clear_flow_box()
        for emoji_char in matches:
            button = Gtk.Button(label=emoji_char)
            button.connect("clicked", self.on_emoji_clicked, emoji_char)
            self.flow_box.add(button)
        self.flow_box.show_all()  # Ensure all buttons are visible

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

        # Perform fuzzy search on emoji descriptions
        if sanitized_query:
            # Find the top 10 closest matches using fuzzywuzzy
            matches = process.extract(
                sanitized_query, self.emoji_descriptions, limit=10
            )

            # Debug: Print the matches
            print("Top 10 Matches:")
            for desc, score in matches:
                print(f"{desc}: {score}")

            # Get the emoji characters for the top matches
            matched_emojis = [
                self.emojis[self.emoji_descriptions.index(desc)]
                for desc, score in matches
                if score > 50
            ]  # Adjust threshold as needed

            # Debug: Print the matched emojis
            print("Matched Emojis:", matched_emojis)

            # Load the top matches into the flow box
            self.load_top_matches(matched_emojis)
        else:
            # If the search bar is empty, show all emojis
            self.load_all_emojis()
