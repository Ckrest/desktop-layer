# Desktop Layer

A lightweight clickable desktop surface for Wayfire and other wlroots-based Wayland compositors.

## Features

- **Click-to-unfocus**: Left-click anywhere on the desktop to unfocus the currently focused window
- **Right-click menu**: Customizable context menu for quick access to applications and commands
- **Layer-shell integration**: Sits on the BOTTOM layer (above wallpaper, below windows)
- **Transparent**: Fully transparent surface that doesn't interfere with your wallpaper

## Requirements

### System Dependencies

```bash
# GTK3 and GObject introspection
sudo apt install python3-gi gir1.2-gtk-3.0

# GTK Layer Shell for Wayland
sudo apt install gir1.2-gtklayershell-0.1
```

### Compositor Requirements

Requires a Wayland compositor that supports the layer-shell protocol:
- Wayfire
- Sway
- Hyprland
- Other wlroots-based compositors

**Note**: Will not work on X11 or compositors without layer-shell support.

## Installation

1. Clone or copy this directory to your preferred location
2. Copy the example config and customize it:
   ```bash
   cp config.json.example config.json
   # Edit config.json with your preferred menu items
   ```
3. (Optional) Set up as a systemd service:
   ```bash
   # Edit desktop-layer.service to update the path to desktop-layer.py
   # Then symlink to systemd
   ln -s /path/to/desktop-layer.service ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable desktop-layer
   ```

## Usage

### Manual Start

```bash
python3 desktop-layer.py
```

### With Custom Config

```bash
python3 desktop-layer.py /path/to/config.json
```

### As systemd Service

```bash
# Enable and start
systemctl --user enable desktop-layer
systemctl --user start desktop-layer

# Check status
systemctl --user status desktop-layer
```

## Configuration

Copy `config.json.example` to `config.json` and customize it. The `config.json` file is gitignored so your personal menu won't be overwritten by updates.

Changes require a service restart: `systemctl --user restart desktop-layer`

### Config Structure

```json
{
  "menu_items": [
    {
      "label": "Terminal",
      "command": "kitty",
      "icon": "utilities-terminal"
    },
    {"separator": true},
    {
      "label": "Settings",
      "submenu": [
        {
          "label": "Display",
          "command": "wdisplays",
          "icon": "preferences-desktop-display"
        }
      ]
    }
  ]
}
```

### Menu Item Options

| Field | Type | Description |
|-------|------|-------------|
| `label` | string | Display text for the menu item |
| `command` | string | Shell command to execute |
| `icon` | string | Icon name from system theme (optional) |
| `separator` | boolean | Creates a separator line when `true` |
| `submenu` | array | Nested array of menu items |

### Default Menu

If no `config.json` exists, a default menu is provided with:
- Terminal
- File Manager
- App Launcher
- Settings submenu (Wayfire Config, Display Settings)

## How It Works

Desktop Layer creates an invisible GTK window using the layer-shell protocol, anchored to all screen edges on the BOTTOM layer. This places it above the wallpaper but below all application windows.

- **Left-click**: The window takes keyboard focus, which automatically removes focus from other windows
- **Right-click**: Displays the configured context menu at the cursor position

## Troubleshooting

### Menu not appearing

Check that GTK Layer Shell is installed:
```bash
python3 -c "import gi; gi.require_version('GtkLayerShell', '0.1')"
```

### GTK deprecation warnings

Warnings about `Gtk.ImageMenuItem` are expected—this is GTK3 deprecation noise. The functionality works correctly.

### Service won't start

Check the logs:
```bash
journalctl --user -u desktop-layer -f
```

## License

MIT
