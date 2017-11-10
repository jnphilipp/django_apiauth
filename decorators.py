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

import json

from django.http import HttpResponseBadRequest, HttpResponseForbidden
from functools import wraps
from hashlib import sha512

from .models import AuthedUser


def authentication_required(func):
    @wraps(func)
    def func_wrapper(request, *args, **kwargs):
        params = request.POST.copy() if request.method == 'POST' \
            else request.GET.copy()
        if 'application/json' == request.META.get('CONTENT_TYPE'):
            params.update(json.loads(request.body.decode('utf-8')))

        if 'token' in params:
            token = params.pop('token')[0]

            try:
                authed_user = AuthedUser.objects.get(token=token)
                authed_user.next_token()
                authed_user.save()
                request.user = authed_user.user
            except AuthedUser.DoesNotExist:
                return HttpResponseForbidden('Authentication failed.')
        else:
            return HttpResponseBadRequest(
                'Required parameter "token" is missing.'
            )

        return func(request, *args, **kwargs)
    return func_wrapper
