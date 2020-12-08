# Generated by Django 2.2.17 on 2020-12-08 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0036_remove_timelocation_time_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelocation',
            name='time_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='timelocation', to='project.TimeOption'),
        ),
    ]
