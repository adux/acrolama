# Generated by Django 2.2.4 on 2019-08-26 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_auto_20190826_1219"),
    ]

    operations = [
        migrations.RemoveField(model_name="staff", name="address",),
        migrations.RemoveField(model_name="staff", name="user",),
        migrations.RemoveField(model_name="teacher", name="address",),
        migrations.RemoveField(model_name="teacher", name="user",),
        migrations.DeleteModel(name="Profile",),
        migrations.DeleteModel(name="Staff",),
        migrations.DeleteModel(name="Teacher",),
    ]
