# Desktop Layer

> AI-assisted development with Claude

A lightweight clickable desktop surface for wlroots-based Wayland compositors (Wayfire, Sway, Hyprland, etc.). Provides right-click context menus and click-to-unfocus functionality.

## Features

- **Click to Unfocus** - Left-click the desktop to unfocus all windows
- **Context Menu** - Right-click shows a customizable menu
- **Wayland Native** - Uses GtkLayerShell for proper layer-shell integration
- **Configurable** - JSON configuration for menu items, icons, and commands
- **Submenus** - Nested menu support for organizing options

## Installation

Requires GTK3, GtkLayerShell, and PyGObject:

```bash
# Ubuntu/Debian
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-gtklayershell-0.1

# Arch Linux
sudo pacman -S python-gobject gtk3 gtk-layer-shell

# Fedora
sudo dnf install python3-gobject gtk3 gtk-layer-shell
```

## Usage

```bash
# Run with default config
python desktop-layer.py

# Run with custom config
python desktop-layer.py /path/to/config.json
```

## Configuration

Copy `config.json.example` to `config.json` and customize:

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
        {"label": "Display", "command": "wdisplays"}
      ]
    }
  ]
}
```

### Menu Item Options

- `label` - Display text
- `command` - Shell command to execute
- `icon` - Icon name (from system icon theme)
- `separator` - Set to `true` for a separator line
- `submenu` - Array of nested menu items

## Running as a Service

Create a systemd user service:

```ini
# ~/.config/systemd/user/desktop-layer.service
[Unit]
Description=Desktop Layer
After=graphical-session.target

[Service]
ExecStart=/usr/bin/python3 /path/to/desktop-layer.py
Restart=on-failure

[Install]
WantedBy=graphical-session.target
```

```bash
systemctl --user enable --now desktop-layer
```

## How It Works

Uses GtkLayerShell to create a fullscreen transparent window on the BOTTOM layer (above wallpaper, below windows). Mouse events are captured to:
- Focus the desktop window (unfocusing everything else)
- Show a popup menu at cursor position

## Built With

- Python
- GTK3
- GtkLayerShell

## License

MIT License - see [LICENSE](LICENSE) for details.
