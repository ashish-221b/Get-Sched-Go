# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Timetable', '0002_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='DeadLine',
        ),
        migrations.AddField(
            model_name='event',
            name='DeadLineDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='DeadLineTime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='EndDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='StartDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='EndTime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='StartTime',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
