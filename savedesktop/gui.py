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

import gi

gi.require_version('Gtk', '3.0')
import argparse
from typing import List
from gi.repository import Gtk


def show_error(msg: str):
    dialog = Gtk.MessageDialog(None,
                               0,
                               Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.CLOSE,
                               "An error has occurred")
    dialog.format_secondary_text(msg)
    dialog.set_title("Save/Restore Virtual Desktop")
    dialog.set_default_size(500, 160)
    dialog.run()
    dialog.destroy()


def show_save_desktop(args: argparse.Namespace, desktop_list: List[str], profile_list: List[str]):
    if len(profile_list) == 0:
        profile_list.append("default")
    if args.profile not in profile_list:
        profile_list.insert(0, args.profile)

    dialog = SaveDialog(args.desktop, desktop_list, args.profile, profile_list)
    response = dialog.run()

    if response != Gtk.ResponseType.OK:
        dialog.destroy()
        exit(0)

    args.desktop = dialog.desktop_combo.get_active()
    args.profile = dialog.profile_combo.get_active_text().strip()
    if len(args.profile) == 0:
        args.profile = "default"
    args.open = dialog.open_checkbox.get_active()

    dialog.destroy()


def show_restore_desktop(args: argparse.Namespace, desktop_list: List[str], profile_list: List[str]):
    dialog = RestoreDialog(args.desktop, desktop_list, args.profile, profile_list)
    response = dialog.run()

    if response != Gtk.ResponseType.OK:
        dialog.destroy()
        exit(0)

    args.desktop = dialog.desktop_combo.get_active()
    args.profile = dialog.profile_combo.get_active_text()

    dialog.destroy()


class SaveDialog(Gtk.Dialog):

    def __init__(self, current_desktop: int, desktop_list: List[str], current_profile, profile_list: List[str]):
        Gtk.Dialog.__init__(self,
                            "Save Virtual Desktop",
                            None, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_border_width(5)

        self.set_icon(self.render_icon(Gtk.STOCK_DIALOG_QUESTION, Gtk.IconSize.DIALOG))

        vbox = self.get_content_area()
        vbox.set_spacing(5)

        hbox = Gtk.HBox(spacing=20)
        vbox.pack_start(hbox, True, True, 0)
        label = Gtk.Label("Desktop:")
        label.set_size_request(70, 20)
        label.set_xalign(0)
        hbox.pack_start(label, False, False, 0)
        self.desktop_combo = Gtk.ComboBoxText()
        for desktop in desktop_list:
            self.desktop_combo.append_text(desktop)
        self.desktop_combo.set_active(current_desktop)
        hbox.pack_start(self.desktop_combo, True, True, 0)

        hbox = Gtk.HBox(spacing=20)
        vbox.pack_start(hbox, True, True, 0)
        label = Gtk.Label("Profile:")
        label.set_size_request(70, 20)
        label.set_xalign(0)
        hbox.pack_start(label, False, False, 0)
        self.profile_combo = Gtk.ComboBoxText()
        for profile in profile_list:
            self.profile_combo.append_text(profile)
        self.profile_combo.set_active(profile_list.index(current_profile))
        hbox.pack_start(self.profile_combo, True, True, 0)

        hbox = Gtk.HBox(spacing=10)
        vbox.pack_start(hbox, True, True, 10)
        label = Gtk.Label()
        label.set_size_request(70, 20)
        hbox.pack_start(label, False, False, 0)
        self.open_checkbox = Gtk.CheckButton("Open JSON file")
        hbox.pack_start(self.open_checkbox, False, False, 0)

        vbox.pack_start(Gtk.HSeparator(), True, True, 0)

        self.show_all()


class RestoreDialog(Gtk.Dialog):

    def __init__(self, current_desktop: int, desktop_list: List[str], current_profile, profile_list: List[str]):
        Gtk.Dialog.__init__(self,
                            "Restore Virtual Desktop",
                            None, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_border_width(5)
        self.set_icon(self.render_icon(Gtk.STOCK_DIALOG_QUESTION, Gtk.IconSize.DIALOG))

        vbox = self.get_content_area()
        vbox.set_spacing(5)

        hbox = Gtk.HBox(spacing=20)
        vbox.pack_start(hbox, True, True, 0)
        label = Gtk.Label("Desktop:")
        label.set_size_request(70, 20)
        label.set_xalign(0)
        hbox.pack_start(label, False, False, 0)
        self.desktop_combo = Gtk.ComboBoxText()
        for desktop in desktop_list:
            self.desktop_combo.append_text(desktop)
        self.desktop_combo.set_active(current_desktop)
        hbox.pack_start(self.desktop_combo, True, True, 0)

        hbox = Gtk.HBox(spacing=20)
        vbox.pack_start(hbox, True, True, 10)
        label = Gtk.Label("Profile:")
        label.set_size_request(70, 20)
        label.set_xalign(0)
        hbox.pack_start(label, False, False, 0)
        self.profile_combo = Gtk.ComboBoxText.new_with_entry()
        for profile in profile_list:
            self.profile_combo.append_text(profile)
        self.profile_combo.set_active(profile_list.index(current_profile))
        hbox.pack_start(self.profile_combo, True, True, 0)

        vbox.pack_start(Gtk.HSeparator(), True, True, 0)

        self.show_all()
