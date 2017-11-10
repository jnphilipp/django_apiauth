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

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone


USER_SETTINGS = getattr(settings, "API_AUTH", {})


APPLICATIONS_ONLY = True
if 'APPLICATIONS_ONLY' in USER_SETTINGS:
    APPLICATIONS_ONLY = USER_SETTINGS['APPLICATIONS_ONLY']


AUTH_REQUEST_TIME = timezone.timedelta(minutes=5)
if 'AUTH_REQUEST_TIME' in USER_SETTINGS:
    AUTH_REQUEST_TIME = USER_SETTINGS['AUTH_REQUEST_TIME']
    if type(AUTH_REQUEST_TIME) != timezone.timedelta:
        raise ImproperlyConfigured(
            'Bad value for AUTH_REQUEST_TIME: %r' % AUTH_REQUEST_TIME
        )


AUTHED_USER_TIME = timezone.timedelta(hours=1)
if 'AUTHED_USER_TIME' in USER_SETTINGS:
    AUTHED_USER_TIME = USER_SETTINGS['AUTHED_USER_TIME']
    if type(AUTHED_USER_TIME) != timezone.timedelta:
        raise ImproperlyConfigured(
            'Bad value for AUTHED_USER_TIME: %r' % AUTHED_USER_TIME
        )
