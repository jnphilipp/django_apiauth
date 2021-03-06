# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 18:39
from __future__ import unicode_literals

from django.db import migrations, models
import django_apiauth.models
import django_apiauth.random


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', django_apiauth.models.SingleLineTextField(unique=True, verbose_name='Name')),
                ('client_id', models.SlugField(unique=True, verbose_name='Client ID')),
                ('secret', django_apiauth.models.SingleLineTextField(default=django_apiauth.random.hex32, unique=True, verbose_name='Client secret')),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
                'ordering': ('name',),
            },
        ),
    ]
