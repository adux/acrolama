# Generated by Django 2.2.10 on 2020-02-17 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("audiovisual", "0005_avatar"),
        ("users", "0007_auto_20200217_1451"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="image",),
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="audiovisual.Avatar"
            ),
        ),
    ]
