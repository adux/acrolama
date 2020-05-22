# Generated by Django 2.2.9 on 2020-02-07 08:37

import booking.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0010_auto_20200128_1052"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="attendance_check",
            field=booking.fields.ArrayField(base_field=models.BooleanField(), size=None),
        ),
        migrations.AlterField(
            model_name="attendance",
            name="attendance_date",
            field=booking.fields.ArrayField(base_field=models.DateField(), size=None),
        ),
    ]
