# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-02 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_auto_20181002_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='content',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]