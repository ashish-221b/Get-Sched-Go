# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedetail',
            name='tutorialSlot',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]