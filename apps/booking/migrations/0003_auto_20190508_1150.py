# Generated by Django 2.0.9 on 2019-05-08 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_auto_20190506_1103'),
        ('accounting', '0002_auto_20190430_0821'),
        ('home', '0032_auto_20190508_1150'),
        ('booking', '0002_auto_20190430_0821'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Booking',
            new_name='Book',
        ),
    ]