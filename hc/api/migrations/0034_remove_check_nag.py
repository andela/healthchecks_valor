# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-14 11:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20170214_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check',
            name='nag',
        ),
    ]