# Generated by Django 2.0.9 on 2019-04-30 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20190430_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoption',
            name='class_end',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='timeoption',
            name='class_start',
            field=models.TimeField(),
        ),
    ]
