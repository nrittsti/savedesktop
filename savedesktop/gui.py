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
import time
from typing import List


def show_error(msg: str):
    subprocess.check_output(["zenity",
                             "--error",
                             "--title=Save Virtual Desktop",
                             "--width=600",
                             "--text={}".format(msg)])


def show_save_desktop(args: argparse.Namespace, desktop_list: List[str], profile_list: List[str]):
    if len(profile_list) == 0:
        profile_list.append("default")
    if args.profile not in profile_list:
        profile_list.insert(0, args.profile)
    else:
        for i in range(len(profile_list)):
            if profile_list[i] == args.profile:
                profile_list[i] = "^{}".format(args.profile)
                break
    if args.desktop is not None:
        desktop_list[args.desktop] = "^{}".format(desktop_list[args.desktop])
    try:
        output = subprocess.check_output(["yad",
                                          "--width=300",
                                          "--form",
                                          "--title=Save Virtual Desktop",
                                          "--field=Desktop:CB",
                                          "!".join(desktop_list),
                                          "--field=Profile:CBE",
                                          "!".join(profile_list),
                                          "--field=Open JSON file:CHK",
                                          "TRUE" if args.open else "FALSE",
                                          ],
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        # Return Code 1 -> The user has pressed Cancel button
        exit(0)
    # parse yad output : b'0 - Workspace 1|default|TRUE|\n'
    values = str(output)[2:-4].split("|")
    args.desktop = int(values[0][0])
    args.profile = values[1].strip()
    if len(args.profile) == 0:
        args.profile = "default"
    args.open = "TRUE" == values[2]
    # avoid wmctrl timing probs
    time.sleep(.100)


def show_restore_desktop(args: argparse.Namespace, desktop_list: List[str], profile_list: List[str]):
    for i in range(len(profile_list)):
        if profile_list[i] == args.profile:
            profile_list[i] = "^{}".format(args.profile)
            break
    desktop_list[args.desktop] = "^{}".format(desktop_list[args.desktop])
    try:
        output = subprocess.check_output(["yad",
                                          "--width=300",
                                          "--form",
                                          "--title=Restore Virtual Desktop",
                                          "--field=Desktop:CB",
                                          "!".join(desktop_list),
                                          "--field=Profile:CB",
                                          "!".join(profile_list),
                                          ],
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        # Return Code 1 -> The user has pressed Cancel button
        exit(0)
    # parse yad output : b'0 - Workspace 1|default|\n'
    values = str(output)[2:-4].split("|")
    args.desktop = int(values[0][0])
    args.profile = values[1].strip()
    # avoid wmctrl timing probs
    time.sleep(.100)
