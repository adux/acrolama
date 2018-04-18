# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-04 08:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20180404_0739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutmemberimage',
            name='member',
        ),
        migrations.AddField(
            model_name='aboutmember',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='about/member/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aboutmember',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='AboutMemberImage',
        ),
    ]