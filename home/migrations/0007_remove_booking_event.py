# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-07 07:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20180501_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='event',
        ),
    ]