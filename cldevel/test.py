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
import subprocess

from cldevel import build

name = 'test'
build_dirs = ['bin', 'lib']


def test(inputdir, clean=True):
    print '= Testing project building ='
    if clean:
        print '* Cleaning build directory'
        build.clean(inputdir)
    print '* Building project'
    build.build(inputdir, debug=True)
    print '* Setup virtual environment'
    os.environ['PATH'] += ':%s' % os.path.join(inputdir, 'bin')
    print '= Running tests ='
    setup_file = open(os.path.join(inputdir, 'setup.json'))
    setup = json.load(setup_file)
    if 'tests' in setup:
        tstdir = os.path.join(inputdir, 'tests')
        if 'colubrid' in setup['tests']:
            for i in setup['tests']['colubrid']:
                srcname = '%s.clsc' % i
                logname = '%s.log' % i
                print '* Running test %s' % i
                logfile = open(os.path.join(tstdir, logname), 'w')
                failed = subprocess.call(['colubrid',
                                       os.path.join(tstdir, srcname)],
                                       stdout=logfile, stderr=logfile)
                logfile.close()
                if failed:
                    print 'Failed'


def do_test(args):
    test(args.input, not args.no_clean)


def add_args(parser):
    parser.add_argument('-nc', '--no-clean', action='store_true',
                        help='Do not clean files')
    return do_test
