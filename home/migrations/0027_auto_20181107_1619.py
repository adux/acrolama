# Generated by Django 2.0.9 on 2018-11-07 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20181002_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='abo',
            field=models.CharField(blank=True, choices=[('SS', 'Single Season Abo'), ('SD', 'Double Season Abo'), ('SC', 'Single Cycle Abo'), ('DC', 'Double Cycle Abo'), ('ST', 'Single Day Ticket')], max_length=8, null=True),
        ),
    ]