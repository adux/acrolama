# Generated by Django 2.2.9 on 2020-01-30 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounting", "0004_auto_20200130_1519"),
    ]

    operations = [
        migrations.RenameField(model_name="invoice", old_name="payed", new_name="paid",),
    ]
