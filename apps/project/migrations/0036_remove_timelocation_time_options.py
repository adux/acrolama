# Generated by Django 2.2.17 on 2020-12-08 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0035_auto_20201208_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timelocation',
            name='time_options',
        ),
    ]
