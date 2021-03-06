# Generated by Django 2.1.2 on 2018-11-07 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20181107_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favDivision',
            field=models.CharField(choices=[('ANY', 'Any'), ('HSD1', 'High School D1'), ('HSD2', 'High School D2'), ('HSJV', 'High School JV'), ('NCAAD1', 'NCAA Division 1'), ('NCAAD2', 'NCAA Division 2'), ('NCAAD3', 'NCAA Division 3')], default='Any', max_length=6),
        ),
        migrations.AddField(
            model_name='profile',
            name='favState',
            field=models.CharField(choices=[('ANY', 'Any'), ('LA', 'Lousiana'), ('OK', 'Oklahoma'), ('TX', 'Texas')], default='Any', max_length=2),
        ),
    ]
