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
import json
import subprocess
import sys
from pathlib import Path
from typing import List

import savedesktop.wmctrl as wmctrl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--open", action="store_true", help="open saved profile")
    parser.add_argument("-p", "--profile", default="default", help="custom profile name")
    parser.add_argument("-d", "--desktop", type=int, default=None, help="desktop number from 0 to n")
    parser.add_argument("--version", action="version", version="0.01")
    args = parser.parse_args()
    try:
        if not wmctrl.check_wmctrl_installation():
            print("wmctrl is not installed", file=sys.stderr)
            exit(-1)
        if not wmctrl.check_xwininfo_installation():
            print("xwininfo is not installed", file=sys.stderr)
            exit(-1)
        if args.desktop is not None:
            desktop = args.desktop
        else:
            desktop = wmctrl.current_desktop()
        window_list = wmctrl.list_window_details(desktop)
        json_path = write_profile(window_list, args.profile)
        if args.open:
            subprocess.call(["xdg-open", str(json_path)])

    except subprocess.CalledProcessError as e:
        print("wmctrl did not work properly: {0}".format(str(e)), file=sys.stderr)
        exit(-1)


def write_profile(window_list: List[dict], profile: str) -> Path:
    # remove unnecessary window properties
    for props in window_list:
        del props["id"]
        del props["desktop"]
        del props["pid"]

    text = json.dumps(window_list, indent=2)
    conf_dir = Path.home().joinpath(".config/savedesktop")
    conf_dir.mkdir(exist_ok=True)
    json_path = conf_dir.joinpath(profile + ".json")
    json_path.write_text(text, "UTF-8")
    return json_path


if __name__ == "__main__":
    main()
