# Generated by Django 2.2.17 on 2020-11-30 16:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0012_invoice_reminder_dates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='reminder_dates',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), blank=True, null=True, size=3),
        ),
    ]