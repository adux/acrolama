# Generated by Django 2.2.12 on 2020-06-13 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0020_auto_20200501_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='informed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]