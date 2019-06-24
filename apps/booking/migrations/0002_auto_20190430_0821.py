# Generated by Django 2.0.9 on 2019-04-30 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='booking',
        #     name='event',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Event'),
        # ),
        migrations.AddField(
            model_name='booking',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.PriceOption'),
        ),
        migrations.AddField(
            model_name='booking',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.TimeOption'),
        ),
    ]
