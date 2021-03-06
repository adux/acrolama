# Generated by Django 2.2.16 on 2020-11-02 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0029_auto_20200926_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='images',
            field=models.ManyToManyField(blank=True, to='audiovisual.Image'),
        ),
        migrations.AlterField(
            model_name='event',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
