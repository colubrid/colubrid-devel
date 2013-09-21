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

name = 'pull'


class Git:
    def __init__(self, name, directory, origin):
        self.name = name
        self.directory = directory
        self.origin = origin
        self.gitdir = os.path.join(directory, '.git')

    def pull(self):
        if os.path.exists(self.directory):
            subprocess.call(['git', '--git-dir=%s' % self.gitdir, 'pull'])
        else:
            subprocess.call(['git', 'clone', self.origin, self.directory])


class GitHub(Git):
    def __init__(self, name, directory, place):
        Git.__init__(self, name, directory, 'git://github.com/%s' % place)


origins = {'git': Git, 'github': GitHub}


def do_pull(parser):
    with open(os.path.join(parser.input, 'setup.json')) as setupfile:
        setup = json.load(setupfile)
    if setup['type'] == 'package':
        repo = Git(None, os.path.abspath(parser.input), None)
        repo.pull()
    else:
        srcdir = os.path.join(parser.input, 'source')
        for name in setup['modules']:
            directory = os.path.join(srcdir, name)
            origin = setup['modules'][name]['type'][0]
            place = setup['modules'][name]['place']
            origins[origin](name, directory, place).pull()


def add_args(parser):
    return do_pull
