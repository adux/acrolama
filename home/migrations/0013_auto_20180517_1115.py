# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-17 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_booking_reduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=3000),
        ),
    ]