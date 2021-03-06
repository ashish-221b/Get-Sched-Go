# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='suggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartTime', models.TimeField(null=True)),
                ('EndTime', models.TimeField(null=True)),
                ('StartDate', models.DateField(null=True)),
                ('Priority', models.CharField(blank=True, default='1', max_length=25)),
                ('Venue', models.CharField(blank=True, max_length=100)),
                ('Hometeam', models.CharField(blank=True, max_length=100)),
                ('Awayteam', models.CharField(blank=True, max_length=100)),
                ('League', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
