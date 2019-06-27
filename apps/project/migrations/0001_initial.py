# Generated by Django 2.2.2 on 2019-06-24 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("address", "0001_initial"),
        ("audiovisual", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Day",
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
                (
                    "day",
                    models.CharField(
                        choices=[
                            ("0", "Monday"),
                            ("1", "Tuesday"),
                            ("2", "Wednesday"),
                            ("3", "Thursday"),
                            ("4", "Friday"),
                            ("5", "Saturday"),
                            ("6", "Sunday"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Level",
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
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("0", "Multilevel"),
                            ("1", "Introduction"),
                            ("2", "Intermediate"),
                            ("3", "Advanced"),
                            ("4", "Profesional"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Location",
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
                ("name", models.CharField(max_length=120)),
                ("max_capacity", models.CharField(blank=True, max_length=5, null=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=2000, null=True),
                ),
                (
                    "indication",
                    models.TextField(blank=True, max_length=2000, null=True),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="address.Address",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="audiovisual.Image",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Policy",
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
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name="PriceOption",
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
                ("abonament", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=30)),
                ("description", models.TextField(max_length=1000)),
                ("reduction", models.BooleanField(default=False)),
                ("price_chf", models.CharField(blank=True, max_length=5, null=True)),
                ("price_euro", models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="TimeOption",
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
                ("name", models.CharField(max_length=20)),
                ("description", models.TextField(max_length=1000)),
                ("class_starttime", models.TimeField(blank=True, null=True)),
                ("class_endtime", models.TimeField(blank=True, null=True)),
                ("open_starttime", models.TimeField()),
                ("open_endtime", models.TimeField()),
                (
                    "regular_days",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.Day",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TimeLocation",
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
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.Location",
                    ),
                ),
                ("time_options", models.ManyToManyField(to="project.TimeOption")),
            ],
        ),
        migrations.CreateModel(
            name="Project",
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
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(max_length=2000)),
                ("todo", models.CharField(blank=True, max_length=120, null=True)),
                ("creationdate", models.DateTimeField(auto_now_add=True)),
                ("manager", models.ManyToManyField(to="users.Staff")),
            ],
        ),
        migrations.CreateModel(
            name="Exception",
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
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("TI", "Time"),
                            ("LO", "Location"),
                            ("TL", "TimeLocation"),
                        ],
                        max_length=15,
                    ),
                ),
                ("description", models.TextField(max_length=2000)),
                ("time_location", models.ManyToManyField(to="project.TimeLocation")),
            ],
        ),
        migrations.CreateModel(
            name="Event",
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
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("fas fa-redo", "Masterclass"),
                            ("fas fa-rocket", "Festival"),
                            ("fas fa-cogs", "Cycle"),
                            ("fas fa-cog", "Workshop"),
                            ("fas fa-star", "Camp"),
                            ("fas fa-seeding", "Retreat"),
                        ],
                        max_length=50,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("event_startdate", models.DateField(blank=True, null=True)),
                ("event_enddate", models.DateField(blank=True, null=True)),
                ("description", models.TextField(max_length=3000)),
                (
                    "max_participants",
                    models.CharField(blank=True, max_length=5, null=True),
                ),
                (
                    "prerequisites",
                    models.TextField(blank=True, max_length=2000, null=True),
                ),
                (
                    "highlights",
                    models.TextField(blank=True, max_length=2000, null=True),
                ),
                ("included", models.TextField(blank=True, max_length=2000, null=True)),
                ("food", models.TextField(blank=True, max_length=2000, null=True)),
                ("published", models.BooleanField()),
                ("registration", models.BooleanField(default=True)),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                ("images", models.ManyToManyField(to="audiovisual.Image")),
                (
                    "level",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.Level",
                    ),
                ),
                (
                    "policy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="project.Policy"
                    ),
                ),
                ("price_options", models.ManyToManyField(to="project.PriceOption")),
                ("staff", models.ManyToManyField(to="users.Staff")),
                ("teacher", models.ManyToManyField(to="users.Teacher")),
                ("time_locations", models.ManyToManyField(to="project.TimeLocation")),
                ("videos", models.ManyToManyField(blank=True, to="audiovisual.Video")),
            ],
        ),
    ]
