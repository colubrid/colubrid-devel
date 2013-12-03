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
from cldevel.python import get_python_paths
import json
import os
import subprocess
import tempfile

name = 'shell'
script = """
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

export PATH=$PATH:"%s"
%s
export PS1="[colubrid-env \W]$ "
"""


def shell(args):
    inputdir = os.path.abspath(args.input)
    setupfile = open(os.path.join(inputdir, 'setup.json'))
    setup = json.load(setupfile)

    if args.build:
        build(args.input, debug=True)

    if setup['type'] == 'package':
        builddir = inputdir
        pythonpath_export = ''
    else:
        builddir = os.path.join(inputdir, 'build')
        pythonpath_export = 'export PYTHONPATH=%s' %\
            ':'.join(get_python_paths(os.path.join(builddir, 'lib')))

    bashrc_path = tempfile.mktemp('.bashrc')
    with open(bashrc_path, 'w') as f:
        f.write(script % (os.path.join(builddir, 'bin'), pythonpath_export))

    subprocess.call(['bash', '--rcfile', bashrc_path])


def add_args(parser):
    parser.add_argument('-b', '--build',
                        help='Build before using virtual environment')
    return shell
