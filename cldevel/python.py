# Copyright (C) 2013 S. Daniel Francis <francis@sugarlabs.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import os
import subprocess

local = """
import os
import sys

for i in @python_paths@:
    sys.path.append(i)

os.environ['PATH'] += ':@bindir@'
"""


def build_python(src, dest, bindir=None, pydirs=None):
    source = open(src, 'r')
    content = source.read()
    source.close()

    if bindir and pydirs:
        header = local.replace('@python_paths@', repr(pydirs))
        header = header.replace('@bindir@', bindir)
    else:
        header = ''

    content = content.replace('# @CLENV@', header)

    output = open(dest, 'w')
    output.write(content)
    output.close()


def get_python_paths(libdir):
    pythondir = os.path.join(libdir, 'python2.7')
    return [pythondir, os.path.join(pythondir, 'site-packages')]


def build_python_package(src, dest):
    olddir = os.getcwd()
    os.chdir(src)
    subprocess.call(['python', 'setup.py', 'install', '--prefix', dest])
    os.chdir(olddir)