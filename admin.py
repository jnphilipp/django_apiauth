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

from django.contrib import admin
from django.forms import TextInput
from .models import Application, AuthedUser, AuthRequest, SingleLineTextField


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ['name', 'client_id', 'secret']
        }),
    ]
    formfield_overrides = {
        SingleLineTextField: {
            'widget': TextInput(attrs={'autocomplete': 'off'})
        },
    }
    list_display = ('name', 'client_id', 'secret', 'updated_at')
    readonly_fields = ('client_id', 'secret')
    search_fields = ('name',)


@admin.register(AuthedUser)
class AuthedUserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ['user', 'token', 'n']
        }),
    ]
    formfield_overrides = {
        SingleLineTextField: {
            'widget': TextInput(attrs={'autocomplete': 'off'})
        },
    }
    list_display = ('user', 'token', 'n', 'updated_at')
    readonly_fields = ('n', 'token')


@admin.register(AuthRequest)
class AuthRequestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ['user', 'timestamp']
        }),
    ]
    list_display = ('user', 'timestamp', 'updated_at')
    list_filters = ('timestamp',)
    readonly_fields = ('timestamp',)
