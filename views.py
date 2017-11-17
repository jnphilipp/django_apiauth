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

from datetime import datetime
from django.contrib.auth import authenticate, get_user_model
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound)
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from hashlib import sha512

from .decorators import authentication_required
from .models import Application, AuthedUser, AuthRequest
from .settings import (APPLICATIONS, REQUIRE_TWO_STEP_AUTHENTICATION,
                       TOKEN_LIVE_TIME)


@csrf_exempt
def request(request):
    """Handels the first POST/GET request in the chain to authenticate a user.

    GET/POST parameters:
    user_id --- main user id e.g. username, email etc.
    client_id --- application client id, required if APPLICATIONS is true
    """
    params = request.POST.copy() if request.method == 'POST' \
        else request.GET.copy()
    if 'application/json' == request.META.get('CONTENT_TYPE'):
        params.update(json.loads(request.body.decode('utf-8')))

    if 'client_id' in params:
        client_id = params.pop('client_id')[0]
        try:
            Application.objects.get(client_id=client_id)
        except Application.DoesNotExist:
            return HttpResponseNotFound(
                'The apllication with "%s" was not found.' % client_id
            )
    elif APPLICATIONS:
        return HttpResponseBadRequest(
            'Required parameter "client_id" is missing.'
        )

    if 'user_id' in params:
        UserModel = get_user_model()
        user_id = params.pop('user_id')[0]

        try:
            user = UserModel._default_manager.get_by_natural_key(user_id)
        except UserModel.DoesNotExist:
            return HttpResponseNotFound(
                'The user with "%s" was not found.' % user_id
            )
    else:
        return HttpResponseBadRequest(
            'Required parameter "user_id" is missing.'
        )

    authrequest, created = AuthRequest.objects.update_or_create(
        user=user,
        defaults={'timestamp': timezone.now()}
    )
    data = {
        'timestamp': authrequest.timestamp.strftime('%Y-%m-%dT%H:%M:%S:%f%z')
    }
    return HttpResponse(json.dumps(data), 'application/json')


@csrf_exempt
def authenticate(request):
    """Handels the second POST/GET request in the chain to authenticate a user.

    GET/POST parameters:
    user_id --- main user id e.g. username, email etc.
    password --- user password
    timestamp --- timestamp from the response of the request to auth request
    client_id --- application client id, required if APPLICATIONS is true
    token --- hash of application secret and timestamp, required if
              APPLICATIONS is true
    """
    params = request.POST.copy() if request.method == 'POST' \
        else request.GET.copy()
    if 'application/json' == request.META.get('CONTENT_TYPE'):
        params.update(json.loads(request.body.decode('utf-8')))

    if 'client_id' in params:
        client_id = params.pop('client_id')[0]
        try:
            application = Application.objects.get(client_id=client_id)
        except Application.DoesNotExist:
            return HttpResponseNotFound(
                'The application with "%s" was not found.' % client_id
            )
    elif APPLICATIONS:
        return HttpResponseBadRequest(
            'Required parameter "client_id" is missing.'
        )

    if 'user_id' in params and 'password' in params:
        UserModel = get_user_model()
        user_id = params.pop('user_id')[0]
        password = params.pop('password')[0]

        try:
            user = UserModel._default_manager.get_by_natural_key(user_id)
            if not user.check_password(password) or not user.is_active:
                return HttpResponseForbidden(
                    'User authentication failed or user is deactivated.'
                )
        except UserModel.DoesNotExist:
            return HttpResponseNotFound(
                'The user with "%s" was not found.' % user_id
            )
    else:
        return HttpResponseBadRequest(
            'Required parameter "user_id" or "password" are missing.'
        )

    if 'timestamp' in params and user:
        timestamp = params.pop('timestamp')[0]

        try:
            timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S:%f%z')
            try:
                auth_request = AuthRequest.objects.get(
                    user=user,
                    timestamp=timestamp
                )
            except AuthRequest.DoesNotExist:
                return HttpResponseForbidden('Authentication failed.')
        except Exception as e:
            return HttpResponseBadRequest(
                'Required parameter "timestamp" has wrong format.'
            )
    elif APPLICATIONS or REQUIRE_TWO_STEP_AUTHENTICATION:
        return HttpResponseBadRequest(
            'Required parameter "timestamp" is missing.'
        )

    if 'token' in params and application:
        recived_token = params.pop('token')[0]
        token = sha512(('%s%s' % (
            application.secret,
            auth_request.timestamp.strftime('%Y-%m-%dT%H:%M:%S:%f%z')
        )).encode('utf-8')).hexdigest()
        if recived_token != token:
            return HttpResponseForbidden('Wrong "token" was given.')
        auth_request.delete()
    elif APPLICATIONS:
        return HttpResponseBadRequest('Required parameter "token" is missing.')

    authed_user, created = AuthedUser.objects.update_or_create(user=user)
    data = {
        'response_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S:%f%z'),
    }
    if TOKEN_LIVE_TIME == 'session':
        data['token'] = authed_user.token
    elif TOKEN_LIVE_TIME == 'request':
        data['n'] = authed_user.n,
        data['secret'] = authed_user.secret
    return HttpResponse(json.dumps(data), 'application/json')


@csrf_exempt
@authentication_required
def heartbeat(request):
    """Handels the POST/GET request to do a heartbeat.
    Useful to prevent auto revoke after AUTHED_USER_TIME of idle.

    GET/POST parameters:
    token --- token: hash of secret and n,
              both received by the authenticate request
    """
    data = {
        'response_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S:%f%z')
    }
    return HttpResponse(json.dumps(data), 'application/json')


@csrf_exempt
@authentication_required
def revoke(request):
    """Handels the POST/GET request to revoke a users authentication.

    GET/POST parameters:
    token --- token: hash of secret and n,
              both received by the authenticate request
    """
    AuthedUser.objects.get(user=request.user).delete()
    data = {
        'response_date': timezone.now().strftime('%Y-%m-%dT%H:%M:%S:%f%z')
    }
    return HttpResponse(json.dumps(data), 'application/json')
