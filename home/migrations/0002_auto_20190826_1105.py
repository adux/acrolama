# Generated by Django 2.2.4 on 2019-08-26 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='infoimage',
            name='general',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Info'),
        ),
        migrations.AddField(
            model_name='aboutimage',
            name='general',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.About'),
        ),
    ]