# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-01 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_auto_20180301_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='publication',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
