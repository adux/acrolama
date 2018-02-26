# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-25 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_aboutgeneral'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('date_description', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='aboutgeneral',
            name='general_dates',
        ),
    ]
