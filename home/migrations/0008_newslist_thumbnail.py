# Generated by Django 2.2.16 on 2020-09-24 09:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20200217_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslist',
            name='thumbnail',
            field=models.ImageField(default=django.utils.timezone.now, editable=False, upload_to='news/thumbs/'),
            preserve_default=False,
        ),
    ]
