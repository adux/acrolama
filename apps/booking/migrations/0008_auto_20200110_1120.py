# Generated by Django 2.2.9 on 2020-01-10 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0007_assistance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assistance",
            name="book",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="booking.Book"
            ),
        ),
    ]
