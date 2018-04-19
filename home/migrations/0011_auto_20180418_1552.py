# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-18 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20180404_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutgeneralimage',
            name='general',
        ),
        migrations.RemoveField(
            model_name='eventimage',
            name='event',
        ),
        migrations.AlterField(
            model_name='aboutgeneral',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='aboutmember',
            name='content',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='event',
            name='cat',
            field=models.CharField(choices=[('fas fa-redo', 'Masterclass'), ('fas fa-rocket', 'Festival'), ('fas fa-cogs', 'Cycle'), ('fas fa-cog', 'Workshop'), ('fas fa-star', 'Camp'), ('fas fa-star', 'Retreat')], default=1, max_length=13),
        ),
        migrations.AlterField(
            model_name='event',
            name='ocurrance',
            field=models.CharField(blank=True, choices=[('Wed', "Wednesday's"), ('Thu', "Thursday's"), ('Sun', "Sunday's"), ('WedSun.', "Wed. & Sunday's"), ('Year', 'Yearly'), ('One', 'One Time')], max_length=8, null=True),
        ),
        migrations.DeleteModel(
            name='AboutGeneralImage',
        ),
        migrations.DeleteModel(
            name='EventImage',
        ),
    ]
