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
import traceback

import savedesktop.check as c
import savedesktop.gui as gui
import savedesktop.profile as p
import savedesktop.wmctrl as wmctrl


def main():
    parser = argparse.ArgumentParser(description='Save virtual desktops (workspaces)')
    parser.add_argument("-g", "--gui", action="store_true", help="gui mode")
    parser.add_argument("-o", "--open", action="store_true", help="show saved profile")
    parser.add_argument("-p", "--profile", default="default", help="profile name")
    parser.add_argument("-d", "--desktop", type=int, default=None, help="desktop number from 0 to n")
    parser.add_argument("--version", action="version", version="0.1.0")
    args = parser.parse_args()
    c.check_dependencies(args)
    try:
        save(args)
    except Exception as e:
        traceback.print_exc()
        if args.gui:
            gui.show_error("{}: {}".format(type(e).__name__, str(e)))
        exit(-1)


def save(args: argparse.Namespace):
    desktop_list = wmctrl.list_desktop()
    c.check_desktop(args, len(desktop_list))
    if args.gui:
        gui.show_save_desktop(args, desktop_list, p.list_profiles())
    window_list = wmctrl.list_window_details(args.desktop)
    json_path = p.write_profile(window_list, args.profile)
    print("profile saved to {}".format(str(json_path)))
    if args.open:
        subprocess.call(["nohup", "xdg-open", str(json_path)], shell=False, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
