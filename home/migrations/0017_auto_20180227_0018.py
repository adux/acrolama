# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-27 00:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20180226_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='ocurrance_event',
            field=models.CharField(blank=True, choices=[('Wed', 'Weekly Wed'), ('Tue', 'Weekly Tue'), ('Sun', 'Weekly Sun'), ('Once', 'One Time Event'), ('Year', 'Yearly')], max_length=7, null=True),
        ),
    ]
