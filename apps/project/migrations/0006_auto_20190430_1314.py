# Generated by Django 2.0.9 on 2019-04-30 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20190430_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time_location',
            field=models.ManyToManyField(related_name='timelocatins', to='project.TimeLocation'),
        ),
    ]
