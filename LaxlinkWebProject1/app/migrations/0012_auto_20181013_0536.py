# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-13 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20181013_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameinfo',
            name='location',
            field=models.CharField(default='Home Team Field', max_length=100),
        ),
    ]