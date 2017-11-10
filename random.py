# -*- coding: utf-8 -*-
# Copyright (C) 2016-1017 Nathanael Philipp (jnphilipp) <mail@jnphilipp.org>
#
# This file is part of django_apiauth.
#
# django_apiauth is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django_apiauth is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django_apiauth. If not, see <http://www.gnu.org/licenses/>.

from os import urandom


def hex(length):
    return ''.join('%02x' % i for i in urandom(length))


def hex32():
    return hex(32)


def s64():
    return abs(9223372036854775807 - int(hex(8), 16))


def u32():
    return abs(2147483647 - int(hex(4), 16))
