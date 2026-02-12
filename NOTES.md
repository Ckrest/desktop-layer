# Desktop Layer - Notes

## Project Structure

**Core functionality:** Generic Wayland layer-shell desktop surface
**Local config:** `config.json` (gitignored) contains personal menu items

## Hardcoded Paths

### Local config.json (Untracked)

The local `config.json` contains paths to Systems tools. These are personal and not distributed:
- Settings Hub, Process Manager, etc.

**After moving Systems:** Edit `config.json` and update paths, then restart service.

### Service File

The service file (`desktop-layer.service`) contains the path to `desktop-layer.py`. Users installing elsewhere must edit this path.

## Dependencies

**GTK3 and Layer Shell:**
- `python3-gi`
- `gir1.2-gtk-3.0`
- `gir1.2-gtklayershell-0.1`

**External tools (optional, for menu items):**
- `wofi` - App launcher
- `wlogout` - Power menu
- `thunar`, `brave-browser`, `gcolor3`, etc.

## Configuration

**File:** `config.json`
**Structure:**
- Menu items array with labels, commands, icons
- Supports submenus
- Supports separators

**Customization:**
Edit `config.json` to add/remove/modify menu items. Changes require service restart.

## Known Issues

**GTK deprecation warnings:**
```
Gtk.ImageMenuItem.set_image is deprecated
Gtk.ImageMenuItem.set_always_show_image is deprecated
```

These are GTK3 deprecations. Functional but should migrate to Gtk.MenuItem with custom rendering eventually.

## Service File

The systemd service file lives in the package and is symlinked to systemd:

```
~/.config/systemd/user/desktop-layer.service -> /home/nick/Systems/desktop/desktop-layer/desktop-layer.service
```

After modifying the service file:
```bash
systemctl --user daemon-reload
systemctl --user restart desktop-layer
```

## Wayfire Integration

This tool is specific to Wayfire/wlroots compositors that support layer-shell protocol. Won't work on X11 or other Wayland compositors without layer-shell.

## Future Plans

Core desktop-layer.py is generic. If extracted:
- Make config.json user-editable
- Add command discovery (PATH lookup)
- Support environment variable expansion in commands
- Add desktop entry support for menu items
