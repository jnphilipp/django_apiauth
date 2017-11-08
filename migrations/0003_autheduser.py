# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 15:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_apiauth.models
import django_apiauth.random


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_apiauth', '0002_authrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('token', django_apiauth.models.SingleLineTextField(unique=True, verbose_name='Token')),
                ('n', models.PositiveIntegerField(default=django_apiauth.random.u32, verbose_name='N')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Authenticated user',
                'verbose_name_plural': 'Authenticated users',
                'ordering': ('user',),
            },
        ),
    ]
