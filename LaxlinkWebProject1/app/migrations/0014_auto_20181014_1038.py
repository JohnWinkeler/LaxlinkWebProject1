# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-14 15:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20181013_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='WinLossRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(choices=[('FALL', 'Fall'), ('SPRING', 'Spring'), ('SUMMER', 'Summer'), ('WINTER', 'Winter'), ('INDOOR', 'Indoor'), ('TRAVEL', 'Travel'), ('NONE', 'None')], default='None', max_length=10)),
                ('wincount', models.IntegerField(default=0)),
                ('losscount', models.IntegerField(default=0)),
                ('year', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='teamdata',
            name='powerrating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='winlossrecord',
            name='teamkey',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='team', to='app.TeamData'),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='winlosslink_loser',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='loserss_record', to='app.WinLossRecord'),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='winlosslink_winner',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='winners_record', to='app.WinLossRecord'),
        ),
    ]
