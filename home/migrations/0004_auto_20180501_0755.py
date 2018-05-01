# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-01 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_info_infoimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='event',
            name='level',
            field=models.CharField(choices=[('A', 'Advanced'), ('B', 'Intermediate'), ('C', 'Introduction'), ('Z', 'Multilevel')], default=1, max_length=1),
        ),
        migrations.AlterField(
            model_name='event',
            name='prerequisites',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]