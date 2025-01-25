import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class TestWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Test GTK Window")
        self.set_default_size(200, 100)

        # Add a button
        button = Gtk.Button(label="Click Me")
        button.connect("clicked", self.on_button_clicked)
        self.add(button)

    def on_button_clicked(self, button):
        print("Button clicked!")


if __name__ == "__main__":
    win = TestWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
