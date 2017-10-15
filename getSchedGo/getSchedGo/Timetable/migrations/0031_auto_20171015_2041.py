# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 15:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0017_auto_20171015_0304'),
        ('Timetable', '0030_auto_20171015_0304'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructorExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('Description', models.CharField(blank=True, max_length=300)),
                ('Venue', models.CharField(blank=True, max_length=100)),
                ('StartTime', models.TimeField(null=True)),
                ('Date', models.DateField(default=datetime.date.today, null=True)),
                ('EndTime', models.TimeField(null=True)),
                ('PreparationDuration', models.CharField(blank=True, choices=[('1', 'Half Hour'), ('2', 'One Hour'), ('3', 'One and Half Hour'), ('4', 'Two Hour')], default='1', max_length=5, null=True)),
                ('UserProfile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
        ),
        migrations.RenameField(
            model_name='instructorclass',
            old_name='StartDate',
            new_name='Date',
        ),
        migrations.RemoveField(
            model_name='instructorclass',
            name='EndDate',
        ),
        migrations.RemoveField(
            model_name='instructorclass',
            name='PreparationDuration',
        ),
        migrations.RemoveField(
            model_name='instructorclass',
            name='PreparationRequired',
        ),
    ]