# Generated by Django 2.1.2 on 2018-10-29 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20181029_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='favTeams',
            field=models.ManyToManyField(blank=True, to='app.TeamData', verbose_name='the favorite teams of the user'),
        ),
    ]
