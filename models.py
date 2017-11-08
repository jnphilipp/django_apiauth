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
from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import random


class SingleLineTextField(models.TextField):
    pass


class Application(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )

    name = SingleLineTextField(
        unique=True,
        verbose_name=_('Name')
    )
    client_id = SingleLineTextField(
        unique=True,
        verbose_name=_('Client ID')
    )
    secret = SingleLineTextField(
        unique=True,
        verbose_name=_('Client secret')
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.generate_tokens()
        super(Application, self).save(*args, **kwargs)

    def generate_tokens(self):
        self.client_id = random.hex(32)
        self.secret = random.hex(32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')


class AuthRequest(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User')
    )
    timestamp = models.DateTimeField(
        verbose_name=_('Timestamp')
    )

    def __str__(self):
        return '%s - %s ' % (
            self.user,
            self.timestamp.strftime('%Y-%m-%dT%H:%M:%S:%f%z')
        )

    class Meta:
        ordering = ('user',)
        unique_together = ('user', 'timestamp')
        verbose_name = _('Auth request')
        verbose_name_plural = _('Auth requests')


class AuthedUser(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User')
    )
    token = SingleLineTextField(
        unique=True,
        verbose_name=_('Token')
    )
    n = models.PositiveIntegerField(
        default=random.u32,
        verbose_name=_('N')
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.token = random.hex(32)
        super(AuthedUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.user

    class Meta:
        ordering = ('user',)
        verbose_name = _('Authenticated user')
        verbose_name_plural = _('Authenticated users')
