# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-21 17:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20180530_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('position', models.CharField(blank=True, max_length=30, null=True)),
                ('content', models.TextField(max_length=1000)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='about/teacher/')),
            ],
        ),
        migrations.RenameField(
            model_name='event',
            old_name='location',
            new_name='loc',
        ),
        migrations.AddField(
            model_name='event',
            name='loc_extra',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Event'),
        ),
    ]