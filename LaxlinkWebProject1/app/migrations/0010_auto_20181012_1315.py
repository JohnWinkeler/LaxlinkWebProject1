# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-12 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20181012_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameinfo',
            name='game_validated',
            field=models.BooleanField(default=False),
        ),
    ]