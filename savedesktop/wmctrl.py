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

import subprocess
import sys
from typing import Dict
from typing import List
from typing import Set

import savedesktop.profile as p


def run_wmctrl(*args: str) -> str:
    arglist = ["wmctrl"]
    arglist.extend(args)
    output = subprocess.check_output(arglist, stderr=subprocess.STDOUT)
    if output is not None:
        output = output.decode(sys.stdout.encoding).strip()
    return output


def list_window_details(desktop: int = None) -> List[dict]:
    result = list()
    out = run_wmctrl("-p", "-G", "-l")
    for line in out.split('\n'):
        if line.endswith("Save Virtual Desktop"):
            continue
        tokens = line.split(maxsplit=7)
        if desktop is not None and desktop != int(tokens[1]):
            continue
        profile = dict()
        profile["id"] = tokens[0]
        profile["desktop"] = int(tokens[1])
        profile["pid"] = int(tokens[2])
        profile["x"] = int(tokens[3])
        profile["y"] = int(tokens[4])
        profile["width"] = int(tokens[5])
        profile["height"] = int(tokens[6])
        p.set_default_values(profile)
        file = open("/proc/{0}/cmdline".format(profile["pid"]), "r")
        try:
            profile["cmd"] = list(filter(str.strip, file.read().split('\0')))
            for i in range(len(profile["cmd"])):
                profile["cmd"][i] = profile["cmd"][i].strip()
        finally:
            file.close()
        fix_window_props(profile)
        xwininfo(profile)
        result.append(profile)
    return result


def fix_window_props(profile: dict):
    if "gnome-terminal-server" in profile["cmd"][0]:
        profile["cmd"] = ["gnome-terminal"]
    if "soffice.bin" in profile["cmd"][0]:
        profile["subtract_extents"] = False
    if profile["cmd"][0].endswith(".exe"):
        profile["subtract_extents"] = False


def list_window_id(desktop: int = None) -> Set[str]:
    window_list = list_window_details(desktop)
    id_set = set()
    for props in window_list:
        id_set.add(props["id"])
    return id_set


def xwininfo(profile: Dict):
    out = subprocess.check_output(["xwininfo", "-id", profile["id"], "-stats", "-wm"], stderr=subprocess.STDOUT)
    if out is not None:
        out = out.decode(sys.stdout.encoding).strip()
    lines = out.split('\n')
    x = 0
    y = 0
    top_decoration = 0
    left_border = 0
    right_border = 0
    bottom_border = 0
    state = list()
    for line in lines:
        line = line.strip()
        if line.startswith("Absolute upper-left X:"):
            # the partition method returns a 3-tuple containing left text, separator, right text
            x = int(line.partition(":")[2].strip())
            continue
        if line.startswith("Absolute upper-left Y:"):
            y = int(line.partition(":")[2].strip())
            continue
        if line == "Maximized Horz":
            state.append("maximized_horz")
            continue
        if line == "Maximized Vert":
            state.append("maximized_vert")
            continue
        if line == "Hidden":
            state.append("hidden")
            continue
        if line.startswith("Frame extents:"):
            extents = line.partition(":")[2].strip().split(", ")
            left_border = int(extents[0])
            left_border = int(extents[1])
            top_decoration = int(extents[2])
            bottom_border = int(extents[3])
            break
    if profile["subtract_extents"]:
        profile["x"] = x - left_border
        profile["y"] = y - top_decoration
    else:
        profile["x"] = x
        profile["y"] = y

    profile["state"] = ",".join(state)


def switch_desktop(desktop: int):
    run_wmctrl("-s", str(desktop))


def get_winid_by_pid(pid: int) -> str:
    out = run_wmctrl("-p", "-l")
    print(pid)
    print(out)
    for line in out.split('\n'):
        tokens = line.split(maxsplit=4)
        if int(tokens[2]) == pid:
            return tokens[0]


def resize_move(winid: str, x: int, y: int, width: int, height: int):
    run_wmctrl("-i", "-r", winid, "-e", "0,{0},{1},{2},{3}".format(x, y, width, height))


def set_state(winid: str, hint: str):
    if hint == "hidden":
        subprocess.call(["xdotool", "windowminimize", winid])
    else:
        run_wmctrl("-i", "-r", winid, "-b", "add," + hint)


def reset_maximized_state(winid: str):
    run_wmctrl("-i", "-r", winid, "-b", "remove,maximized_vert,maximized_horz")


def current_desktop() -> int:
    out = run_wmctrl("-d")
    for line in out.split('\n'):
        if '*' in line:
            return int(line[0])
    return 0


def list_desktop() -> List[str]:
    out = run_wmctrl("-d")
    result = list()
    for line in out.split('\n'):
        items = line.split("  ")
        result.append("{} - {}".format(items[0], items[-1]))
    return result
