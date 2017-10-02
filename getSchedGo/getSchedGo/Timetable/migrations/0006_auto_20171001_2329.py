# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Timetable', '0005_auto_20171001_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='Type',
            field=models.CharField(choices=[('A', 'Official Classes'), ('B', 'Study Acads'), ('C', 'Extra Study'), ('D', 'ExtraCurriculars'), ('E', 'Misc.')], default='E', max_length=25),
        ),
    ]
