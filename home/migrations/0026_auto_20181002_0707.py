# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-02 07:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20181002_0649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='reduction',
            field=models.CharField(blank=True, choices=[('ST', 'Student Price'), ('NM', 'Normal Price')], max_length=12, null=True),
        ),
    ]