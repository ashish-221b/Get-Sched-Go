# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 17:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0017_auto_20171015_0304'),
        ('courses', '0003_auto_20171015_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedetail',
            name='Student',
            field=models.ManyToManyField(related_name='Student_List', to='profiles.profile'),
        ),
    ]
