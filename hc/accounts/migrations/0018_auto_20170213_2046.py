# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-13 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20170213_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='daily_schedule',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='monthly_schedule',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='profile',
            name='weekly_schedule',
            field=models.IntegerField(default=7),
        ),
    ]
