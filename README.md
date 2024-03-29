# SaveDesktop

A CLI tool for saving and restoring virtual linux desktops.

Stage of development: discotinued

> SaveDesktop needs the deprecated xorg display server.  
> Xorg is almost unmaintened and will be phased out by most of the mayor Linux destributions.  
> The default desktop session is now the Wayland session.  
> Alternatives:
> - [Sway](https://github.com/Nama/swayrst)
> - [KDE Plasma Window Rules](https://userbase.kde.org/KWin_Rules_Window_Attributes) 

Main features: 
-------------------
  - Dumping window geometry and hints to human readable JSON files
  - Apply the saved layout to any virtual desktop
  - Command Line Interface
  - GTK Interface
  
Dependencies:
----------------------

 - X Window Manager that implement the EWMH specification
 - wmctrl (https://sites.google.com/site/tstyblo/wmctrl/)
 - xwininfo (for getting window geometry and extents)
 - xdotool (for hiding windows)
 - Python 3.7
 - python-setuptools
 - python-gobject
 - gtk3

Compatibility:
--------------------------

Tested DEs:

| Desktop Enviroment | Version | Window Manager |
|--------------------|---------|----------------|
| Cinnamon           | 4       | Muffin         |
| LXQT               | 0.13    | OpenBox        |
| Mate               | 1.20    | Marco          |
| Plasma             | 5       | Kwin           |
| XFCE               | 4       | Xfwm           |


Tested Applications:

- Caja
- Chromium
- Dolphin
- Falkon
- Firefox
- Galculator 
- Gedit
- Kate
- Konsole
- Leafpad
- Libre Office
- Lxterminal
- Mate-Terminal
- Midori
- Mousepad
- Nemo
- Pluma
- Qpdview
- Thunar (remove --daemon option)
- VLC
- Wine Apps
- Xed
- Xreader

Incompatible:
--------------------------

- Gimp, setting gemometry failed

Installation:
--------------------------

Arch Linux AUR package:

https://aur.archlinux.org/packages/savedesktop/

For manual installation use the following command:

```
$ sudo python setup.py install --optimize=1
```

Usage:
--------------------------

dump a desktop:

```
$ svd -d 0 -p profile1 -o
```
options:

`-d 0` dump first desktop

`-p profile1` save to ~/.config/savedesktop/profile1.json 

`-o` open in default editor

save with gui:

```
$ svd --gui
```

restore a desktop:

```
$ rvd -d 1 -p profile1
```

`-d 1` restore to second desktop

`-p profile1` load ~/.config/savedesktop/profile1.json

restore with gui dialog:

```
$ rvd --gui
```

Profiles:
--------------------

Profile files are stored in '~/.config/savedesktop'

```
[
  {
    "x": 403,
    "y": 219,
    "width": 1094,
    "height": 599,
    "timeout": 5,
    "cmd": [
      "nemo"
    ],
    "state": ""
  }
]
```

The following state properties are supported:
- maximized_vert
- maximized_horz
- shaded
- hidden
- fullscreen

Project Web site:
--------------------

https://github.com/nrittsti/savedesktop/

--------------------------------------------------------------------------------
Licence:
--------------------------------------------------------------------------------
 

This program is free software:
you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2018 Nico Rittstieg

--------------------------------------------------------------------------------
End of document
