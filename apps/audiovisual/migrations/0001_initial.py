# Generated by Django 2.2.4 on 2019-08-26 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=50)),
                (
                    "description",
                    models.TextField(blank=True, max_length=230, null=True),
                ),
                ("image", models.ImageField(upload_to="images/")),
            ],
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=50)),
                (
                    "description",
                    models.TextField(blank=True, max_length=230, null=True),
                ),
                ("link", models.CharField(max_length=300)),
                ("image", models.ImageField(upload_to="videos/")),
            ],
        ),
    ]
