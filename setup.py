#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

from distutils.core import setup

setup(name='colubrid-devel',
      version='0.1',
      description='Colubrid development tools',
      author='Daniel Francis',
      author_email='francis@sugarlabs.org',
      license='GPLv3',
      url='http://github.com/colubrid/colubrid-devel',
      packages=['cldevel'],
      scripts=['colubrid-project']
)
