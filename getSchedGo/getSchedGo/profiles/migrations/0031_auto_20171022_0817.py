# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0030_auto_20171022_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='contact',
            field=models.IntegerField(null=True),
        ),
    ]