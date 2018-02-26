# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-25 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20180225_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutdate',
            name='date_description',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aboutdate',
            name='date_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aboutdate',
            name='date_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]