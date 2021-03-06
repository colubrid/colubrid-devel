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

import json
import os
import shutil
import stat

from cldevel import python

from cldevel.fsutils import mkdir
from cldevel.fsutils import rmdir

name = 'build'

cleandirs = ['bin', 'lib']

def build_scripts(scripts, srcdir, bindir, libdir=None, debug=False):
    if 'python' in scripts:
        for i in scripts['python']:
            name = '%s.py' % i
            origin = os.path.join(srcdir, name)
            destination = os.path.join(bindir, i)
            python.build_python(origin, destination, bindir, libdir)
            os.chmod(destination,
                     stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                     stat.S_IRGRP | stat.S_IXGRP |
                     stat.S_IROTH | stat.S_IXOTH)
    if debug and 'debug' in scripts:
        build_scripts(scripts['debug'], srcdir, bindir, libdir, debug=True)


def build(inputdir, outputdir=None, debug=False):
    setupfile = open(os.path.join(inputdir, 'setup.json'))
    setup = json.load(setupfile)
    dest = outputdir or inputdir
    mkdir(dest)

    if setup['type'] == 'package':
        # Libraries
        libraries = os.path.join(inputdir, 'library')
        lib = os.path.join(dest, 'lib')
        pythonlibs = python.get_python_paths(lib)
        mkdir(lib)
        if 'python' in setup['libs']:
            for path in pythonlibs:
                mkdir(path)
            for i in setup['libs']['python']:
                origin = os.path.join(libraries, i)
                destination = os.path.join(pythonlibs[-1], i)
                shutil.copytree(origin, destination)

        # Executable scripts
        scripts = os.path.join(inputdir, 'src')
        bins = os.path.join(dest, 'bin')
        mkdir(bins)
        build_scripts(setup['scripts'], scripts, bins,
                    pythonlibs if lib != '/usr/lib' else None, debug)
    else:
        builddir = os.path.join(inputdir, 'build')
        mkdir(builddir)
        for module in setup['modules']:
            print 'Building %s' % module
            builders[setup['modules'][module]['type'][1]](
                os.path.join(inputdir, 'source', module),
                builddir)


builders = {'colubrid': build,
            'python': python.build_python_package}


def clean(outputdir):
    [rmdir(os.path.join(outputdir, i)) for i in cleandirs]


def do_build(args):
    inputdir = os.path.abspath(args.input)
    outputdir = os.path.abspath(args.output) or inputdir
    if args.clean:
        clean(outputdir)
    build(inputdir, outputdir, args.debug)


def add_args(parser):
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Build in debug mode')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='Clean built files (if any) before building.')
    parser.add_argument('-o', '--output', metavar='OUTPUT', default='')
    return do_build
