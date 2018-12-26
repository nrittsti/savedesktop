#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# This file is part of savedesktop.
# A CLI tool for saving and restoring virtual linux desktops.
#
# Copyright (C) 2018 Nico Rittstieg
#
# This program is free software:
# you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

import argparse
import subprocess
import sys
import time
import traceback
from typing import Dict

import savedesktop.check as c
import savedesktop.gui as gui
import savedesktop.profile as p
import savedesktop.wmctrl as wmctrl


def main():
    parser = argparse.ArgumentParser(description='Restore virtual desktops (workspaces)')
    parser.add_argument("-g", "--gui", action="store_true", help="gui mode")
    parser.add_argument("-p", "--profile", default="default", help="profile name")
    parser.add_argument("-d", "--desktop", type=int, default=0, help="target desktop number from 0 to n")
    parser.add_argument("--version", action="version", version="0.1.0")
    args = parser.parse_args()
    c.check_dependencies(args)
    try:
        restore(args)
    except Exception as e:
        traceback.print_exc()
        if args.gui:
            gui.show_error("{}: {}".format(type(e).__name__, str(e)))
        exit(-1)


def restore(args: argparse.Namespace):
    desktop_list = wmctrl.list_desktop()
    c.check_desktop(args, len(desktop_list))
    if args.gui:
        gui.show_restore_desktop(args, desktop_list, p.list_profiles())
    print("Restoring profile: {}".format(args.profile))
    try:
        window_list = p.read_profile(args.profile)
    except FileNotFoundError as e:
        print("profile '{0}' not found".format(e.filename), file=sys.stderr)
        exit(-1)
    wmctrl.switch_desktop(args.desktop)
    for props in window_list:
        open_window(args.desktop, props)


def open_window(desktop: int, profile: Dict) -> bool:
    window_ids = wmctrl.list_window_id(desktop)
    print("Popen: {}".format(" ".join(profile["cmd"])))
    profile["cmd"].insert(0, "nohup")
    subprocess.Popen(profile["cmd"], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    timeout = 5 if (profile["timeout"] is None) else profile["timeout"]
    for x in range(timeout * 10):
        time.sleep(.10)
        new_ids = wmctrl.list_window_id(desktop) - window_ids
        if len(new_ids) == 0:
            continue
        win_id = new_ids.pop()
        wmctrl.reset_maximized_state(win_id)
        print("Apply: x={} y={} w={} h={} state={}".format(profile["x"], profile["y"],
                                                           profile["width"], profile["height"], profile["state"]))
        wmctrl.resize_move(win_id, profile["x"], profile["y"], profile["width"], profile["height"])
        if len(profile["state"]) > 0:
            wmctrl.set_state(win_id, profile["state"])
        return True
    print("timeout reached")
    return False


if __name__ == "__main__":
    main()
