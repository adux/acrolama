# Generated by Django 2.0.9 on 2019-05-02 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_auto_20190502_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Level'),
        ),
    ]
