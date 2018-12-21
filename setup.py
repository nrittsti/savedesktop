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

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='savedesktop',
    version='0.0.1',
    entry_points={
        'console_scripts': ['sd=savedesktop.sd:main', 'rd=savedesktop.rd:main']
    },
    author='Nico Rittstieg',
    description='cli script to save and restore virtual desktops',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/nrittsti/sd',
    packages=setuptools.find_packages(),
    license="GPL",
    keywords=['window manager', 'wmctrl', 'desktop'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPL License',
        'Operating System :: Linux',
        'Intended Audience :: End Users/Desktop',
    ),
)
