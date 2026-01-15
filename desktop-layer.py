#!/usr/bin/env python3
"""
Desktop Layer - A lightweight clickable desktop surface for Wayfire/wlroots compositors.

Creates an invisible window on the BOTTOM layer that:
- Left-click: Takes focus (unfocusing the previous window)
- Right-click: Shows a customizable context menu
"""

import gi
import json
import os
import subprocess
import signal
import sys

gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GtkLayerShell, GLib

# Default configuration
DEFAULT_CONFIG = {
    "menu_items": [
        {
            "label": "Open Terminal",
            "command": "kitty",
            "icon": "utilities-terminal"
        },
        {
            "label": "File Manager",
            "command": "thunar",
            "icon": "system-file-manager"
        },
        {"separator": True},
        {
            "label": "App Launcher",
            "command": "wofi --show drun",
            "icon": "view-grid-symbolic"
        },
        {"separator": True},
        {
            "label": "Settings",
            "submenu": [
                {
                    "label": "Wayfire Config",
                    "command": "wcm",
                    "icon": "preferences-system"
                },
                {
                    "label": "Display Settings",
                    "command": "wlr-randr-gui || wdisplays",
                    "icon": "preferences-desktop-display"
                }
            ]
        }
    ]
}


class DesktopLayer:
    def __init__(self, config_path=None):
        self.config = self.load_config(config_path)
        self.window = None
        self.menu = None
        self.setup_window()
        self.setup_menu()

    def load_config(self, config_path):
        """Load configuration from file or use defaults."""
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    config = DEFAULT_CONFIG.copy()
                    config.update(user_config)
                    return config
            except Exception as e:
                print(f"Warning: Could not load config from {config_path}: {e}")
                print("Using default configuration.")
        return DEFAULT_CONFIG

    def setup_window(self):
        """Create the transparent layer-shell window."""
        self.window = Gtk.Window()

        # Initialize layer shell
        GtkLayerShell.init_for_window(self.window)

        # Set to BOTTOM layer (above wallpaper, below windows)
        GtkLayerShell.set_layer(self.window, GtkLayerShell.Layer.BOTTOM)

        # Anchor to all edges (fills entire screen)
        GtkLayerShell.set_anchor(self.window, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self.window, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.set_anchor(self.window, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self.window, GtkLayerShell.Edge.RIGHT, True)

        # No exclusive zone (don't reserve space)
        GtkLayerShell.set_exclusive_zone(self.window, -1)

        # Accept keyboard focus when clicked
        GtkLayerShell.set_keyboard_mode(
            self.window,
            GtkLayerShell.KeyboardMode.ON_DEMAND
        )

        # Make window transparent
        self.window.set_app_paintable(True)
        screen = self.window.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.window.set_visual(visual)

        # Create event box to capture clicks
        event_box = Gtk.EventBox()
        event_box.set_above_child(False)
        event_box.set_visible_window(False)
        event_box.connect('button-press-event', self.on_button_press)

        self.window.add(event_box)

        # Connect to draw signal for transparency
        self.window.connect('draw', self.on_draw)
        self.window.connect('destroy', Gtk.main_quit)

    def on_draw(self, widget, cr):
        """Draw fully transparent background."""
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(1)  # CAIRO_OPERATOR_SOURCE
        cr.paint()
        return False

    def on_button_press(self, widget, event):
        """Handle mouse button clicks."""
        if event.button == 1:  # Left click
            # Just taking focus is enough to unfocus other windows
            # The window already has ON_DEMAND keyboard mode
            self.window.present()
            return True

        elif event.button == 3:  # Right click
            self.show_menu(event)
            return True

        return False

    def setup_menu(self):
        """Build the right-click context menu from config."""
        self.menu = Gtk.Menu()
        self.build_menu_items(self.menu, self.config.get('menu_items', []))
        self.menu.show_all()

    def build_menu_items(self, menu, items):
        """Recursively build menu items."""
        for item in items:
            if item.get('separator'):
                menu.append(Gtk.SeparatorMenuItem())
            elif 'submenu' in item:
                # Create submenu
                submenu_item = Gtk.MenuItem(label=item['label'])
                submenu = Gtk.Menu()
                self.build_menu_items(submenu, item['submenu'])
                submenu_item.set_submenu(submenu)
                menu.append(submenu_item)
            else:
                # Regular menu item
                menu_item = self.create_menu_item(item)
                menu.append(menu_item)

    def create_menu_item(self, item):
        """Create a single menu item with optional icon."""
        if item.get('icon'):
            menu_item = Gtk.ImageMenuItem(label=item['label'])
            icon = Gtk.Image.new_from_icon_name(item['icon'], Gtk.IconSize.MENU)
            menu_item.set_image(icon)
            menu_item.set_always_show_image(True)
        else:
            menu_item = Gtk.MenuItem(label=item['label'])

        command = item.get('command')
        if command:
            menu_item.connect('activate', self.on_menu_activate, command)

        return menu_item

    def on_menu_activate(self, widget, command):
        """Execute command when menu item is clicked."""
        try:
            # Run command in background, detached from this process
            subprocess.Popen(
                command,
                shell=True,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"Error executing command '{command}': {e}")

    def show_menu(self, event):
        """Display the context menu at cursor position."""
        self.menu.popup_at_pointer(event)

    def run(self):
        """Start the desktop layer."""
        self.window.show_all()
        print("Desktop Layer running on BOTTOM layer")
        print("  Left-click: Unfocus windows")
        print("  Right-click: Context menu")
        Gtk.main()


def main():
    # Handle SIGTERM/SIGINT gracefully
    signal.signal(signal.SIGTERM, lambda *_: Gtk.main_quit())
    signal.signal(signal.SIGINT, lambda *_: Gtk.main_quit())

    # Determine config path
    config_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(config_dir, 'config.json')

    # Allow override via command line
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    desktop = DesktopLayer(config_path)
    desktop.run()


if __name__ == '__main__':
    main()
