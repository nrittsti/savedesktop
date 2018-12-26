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

import json
from pathlib import Path
from typing import Dict
from typing import List


def list_profiles() -> List[str]:
    pdir = Path.home().joinpath(".config/savedesktop")
    result = list()
    if pdir.exists():
        files = pdir.glob("*.json")
        for file in files:
            result.append(file.stem)
    return result


def read_profile(profile: str) -> List[dict]:
    json_path = Path.home().joinpath(".config/savedesktop/" + profile + ".json")
    text = json_path.read_text("UTF-8")
    result = json.loads(text)
    for profile in result:
        set_default_values(profile)
    return result


def write_profile(window_list: List[dict], profile: str) -> Path:
    # remove unnecessary window properties
    for props in window_list:
        del props["id"]
        del props["desktop"]
        del props["pid"]
        del props["subtract_extents"]

    text = json.dumps(window_list, indent=2)
    conf_dir = Path.home().joinpath(".config/savedesktop")
    conf_dir.mkdir(exist_ok=True)
    json_path = conf_dir.joinpath(profile + ".json")
    json_path.write_text(text, "UTF-8")
    return json_path


def set_default_values(profile: Dict):
    profile.setdefault("timeout", 5)
    profile.setdefault("subtract_extents", True)
