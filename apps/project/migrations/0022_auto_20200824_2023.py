# Generated by Django 2.2.13 on 2020-08-24 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0021_auto_20200513_1347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='teacher',
            new_name='teachers',
        ),
    ]
