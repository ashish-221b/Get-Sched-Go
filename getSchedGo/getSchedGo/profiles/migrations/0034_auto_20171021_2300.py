# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 17:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0033_auto_20171021_2259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='NBAenthu',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='crickenthu',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='footballenthu',
        ),
    ]