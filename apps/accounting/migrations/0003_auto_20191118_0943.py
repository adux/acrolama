# Generated by Django 2.2.6 on 2019-11-18 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounting", "0002_auto_20190826_1105"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partner",
            name="account",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="accounting.Account",
            ),
        ),
    ]
