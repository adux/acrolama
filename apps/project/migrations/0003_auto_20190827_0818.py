# Generated by Django 2.2.4 on 2019-08-27 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0002_auto_20190826_1105"),
    ]

    operations = [
        migrations.CreateModel(
            name="Discipline",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID",),),
                ("name", models.CharField(max_length=20)),
                ("description", models.TextField(blank=True, max_length=1000, null=True),),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="project",
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to="project.Project",),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="discipline",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="project.Discipline",
            ),
        ),
    ]
