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

import savedesktop.gui as gui
import savedesktop.wmctrl as wmctrl


def check_dependencies(args: argparse.Namespace):
    if not check_wmctrl_installation():
        print("wmctrl is not installed", file=sys.stderr)
        if args.gui:
            gui.show_error("wmctrl is not installed")
        exit(-1)
    if not check_xwininfo_installation():
        print("xwininfo is not installed", file=sys.stderr)
        if args.gui:
            gui.show_error("xwininfo is not installed")
        exit(-1)
    if not check_xdotool_installation():
        print("xdotool is not installed", file=sys.stderr)
        if args.gui:
            gui.show_error("xdotool is not installed")
        exit(-1)


def check_wmctrl_installation():
    try:
        subprocess.call(["wmctrl", "--version"], stdout=subprocess.DEVNULL)
        return True
    except FileNotFoundError as e:
        return False


def check_xwininfo_installation():
    try:
        subprocess.call(["xwininfo", "-version"], stdout=subprocess.DEVNULL)
        return True
    except FileNotFoundError as e:
        return False


def check_xdotool_installation():
    try:
        subprocess.call(["xdotool", "--version"], stdout=subprocess.DEVNULL)
        return True
    except FileNotFoundError as e:
        return False


def check_desktop(args: argparse.Namespace, desktop_count: int):
    if args.desktop is not None:
        if args.desktop < 0 or args.desktop >= desktop_count:
            msg = "Desktop '{}' is invalid! Choose between 0 and {}".format(args.desktop, desktop_count - 1)
            print(msg, file=sys.stderr)
            if args.gui:
                gui.show_error(msg)
            exit(-1)
    else:
        args.desktop = wmctrl.current_desktop()
