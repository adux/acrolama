# Generated by Django 2.0.9 on 2019-05-04 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_auto_20190504_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='firs_name',
            new_name='first_name',
        ),
    ]