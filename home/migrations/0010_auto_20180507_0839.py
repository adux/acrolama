# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-07 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20180507_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='pay_till',
            field=models.DateField(blank=True, null=True),
        ),
    ]
