# Generated by Django 2.2.11 on 2020-04-04 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_auto_20200404_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('MC', 'Masterclass'), ('FT', 'Festival'), ('CY', 'Cycle'), ('WS', 'Workshop'), ('CA', 'Camp'), ('RT', 'Retreat')], max_length=50),
        ),
    ]