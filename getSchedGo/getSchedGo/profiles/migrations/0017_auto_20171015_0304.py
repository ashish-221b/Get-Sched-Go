# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 21:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_merge_20171014_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='lastSuggestion',
            field=models.DateField(default=datetime.date(2017, 10, 10), null=True),
        ),
    ]
