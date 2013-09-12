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

from cldevel.build import build
import os
import subprocess
import tempfile

name = 'shell'
script = """
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

export PATH=$PATH:"%s"
export PS1="[colubrid-env \W]$ "
"""


def shell(args):
    if not args.no_build:
        build(args.input, debug=True)

    bashrc_path = tempfile.mktemp('.bashrc')
    with open(bashrc_path, 'w') as f:
        f.write(script % os.path.abspath(os.path.join(args.input, 'bin')))

    subprocess.call(['bash', '--rcfile', bashrc_path])


def add_args(parser):
    parser.add_argument('-nb', '--no-build',
                        help='Do not build before using virtual environment')
    return shell
