# Generated by Django 2.2.11 on 2020-03-30 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0014_auto_20200330_2051"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="max_participants",
            field=models.PositiveIntegerField(blank=True, default=2, null=True),
        ),
        migrations.AlterField(
            model_name="location",
            name="max_capacity",
            field=models.PositiveIntegerField(blank=True, default=2, null=True),
        ),
    ]
