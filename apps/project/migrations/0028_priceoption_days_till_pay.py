# Generated by Django 2.2.16 on 2020-09-16 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0027_auto_20200916_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='priceoption',
            name='days_till_pay',
            field=models.IntegerField(default=10, verbose_name='Days to Pay'),
        ),
    ]