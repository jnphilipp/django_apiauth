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

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import AuthedUser, AuthRequest


@receiver(pre_save, sender=AuthRequest)
def delete_old_auth_requests(sender, **kwargs):
    """Delete authentication requests after 5 minutes."""
    AuthRequest.objects.filter(
        timestamp__lte=(timezone.now() - timezone.timedelta(minutes=5))
    ).delete()


@receiver(pre_save, sender=AuthRequest)
def delete_old_authed_users(sender, **kwargs):
    """Logs users out after one hour of inactivity."""
    AuthedUser.objects.filter(
        updated_at__lte=(timezone.now() - timezone.timedelta(hours=1))
    ).delete()
