# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-13 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_check_nag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='nag',
            field=models.DurationField(null=True),
        ),
    ]