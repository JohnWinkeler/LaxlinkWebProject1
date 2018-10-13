# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-12 15:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homeTeam', models.CharField(max_length=100)),
                ('awayTeam', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('gameType', models.CharField(choices=[('S', 'Scrimmage'), ('R', 'Regular Season'), ('P', 'Playoff'), ('C', 'Championship'), ('T', 'Tournament')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='ScoreInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TeamData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('coach', models.CharField(max_length=100)),
                ('contactName', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=20)),
                ('conference', models.CharField(max_length=20)),
                ('division', models.CharField(choices=[('HSD1', 'High School D1'), ('HSD2', 'High School D2'), ('HSJV', 'High School JV'), ('NCAAD1', 'NCAA Division 1'), ('NCAAD2', 'NCAA Division 2'), ('NCAAD3', 'NCAA Division 3')], max_length=6)),
            ],
        ),
    ]
