# Generated by Django 2.2.10 on 2020-03-22 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0013_quotation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quotation",
            name="acrolama_profit",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="quotation",
            name="teachers_profit",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]