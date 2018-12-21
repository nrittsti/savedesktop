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
import time
from pathlib import Path
from typing import List

import savedesktop.wmctrl as wmctrl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--profile", default="default", help="profile name")
    parser.add_argument("-d", "--desktop", type=int, default=0, help="target desktop number from 0 to n")
    parser.add_argument("--version", action="version", version="0.01")
    args = parser.parse_args()
    window_list = list()
    try:
        window_list = read_profile(args.profile)
    except FileNotFoundError as e:
        print("profile '{0}' not found".format(e.filename), file=sys.stderr)
        exit(-1)
    try:
        if not wmctrl.check_wmctrl_installation():
            print("wmctrl is not installed", file=sys.stderr)
            exit(-1)
        wmctrl.switch_desktop(args.desktop)
        for props in window_list:
            open_window(args.desktop, props)
    except subprocess.CalledProcessError as e:
        print("wmctrl did not work properly: {0}".format(str(e)), file=sys.stderr)
        exit(-1)


def read_profile(profile: str) -> List[dict]:
    json_path = Path.home().joinpath(".config/savedesktop/" + profile + ".json")
    text = json_path.read_text("UTF-8")
    result = json.loads(text)
    return result


def open_window(desktop: int, props: dict) -> bool:
    window_ids = wmctrl.list_window_id(desktop)
    print(window_ids)
    subprocess.Popen(props["cmd"], shell=False)
    for x in range(10):
        time.sleep(.50)
        new_ids = wmctrl.list_window_id(desktop) - window_ids
        if len(new_ids) == 0:
            continue
        win_id = new_ids.pop()
        wmctrl.resize_move(win_id, props["x"], props["y"], props["width"], props["height"])
        if len(props["state"]) > 0:
            wmctrl.set_state(win_id, props["state"])
        return True
    return False


if __name__ == "__main__":
    main()
