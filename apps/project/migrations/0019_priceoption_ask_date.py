# Generated by Django 2.2.12 on 2020-04-21 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_auto_20200421_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='priceoption',
            name='ask_date',
            field=models.BooleanField(default=False),
        ),
    ]