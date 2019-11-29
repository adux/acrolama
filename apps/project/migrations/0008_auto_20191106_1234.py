# Generated by Django 2.2.6 on 2019-11-06 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0007_auto_20191021_1709"),
    ]

    operations = [
        migrations.RenameModel(old_name="Exception", new_name="Irregularity",),
        migrations.AlterModelOptions(
            name="irregularity",
            options={"verbose_name_plural": "Irregularities"},
        ),
        migrations.AlterModelOptions(
            name="policy", options={"verbose_name_plural": "Policies"},
        ),
        migrations.RenameField(
            model_name="event",
            old_name="exceptions",
            new_name="irregularities",
        ),
        migrations.AlterField(
            model_name="timeoption",
            name="name",
            field=models.CharField(max_length=30),
        ),
    ]