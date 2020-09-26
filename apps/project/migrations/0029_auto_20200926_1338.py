# Generated by Django 2.2.16 on 2020-09-26 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0028_priceoption_days_till_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='discipline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project.Discipline'),
        ),
        migrations.AlterField(
            model_name='event',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project.Level'),
        ),
        migrations.AlterField(
            model_name='event',
            name='policy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='project.Policy'),
        ),
        migrations.AlterField(
            model_name='event',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='project.Project'),
        ),
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='address.Address'),
        ),
        migrations.AlterField(
            model_name='location',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='audiovisual.Image'),
        ),
    ]
