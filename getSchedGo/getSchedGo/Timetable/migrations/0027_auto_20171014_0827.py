# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 02:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Timetable', '0026_instructorassignment_instructorclass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='DeadLineDate',
            field=models.DateField(blank=True, default=datetime.date(2017, 10, 17), null=True),
        ),
        migrations.AlterField(
            model_name='instructorassignment',
            name='DeadLineDate',
            field=models.DateField(blank=True, default=datetime.date(2017, 10, 17), null=True),
        ),
    ]
