# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20171015_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedetail',
            name='Slot',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
