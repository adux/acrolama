# Generated by Django 2.2.4 on 2019-08-26 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID",),),
                ("name", models.CharField(max_length=30)),
                (
                    "balance",
                    models.CharField(
                        choices=[("AS", "Assets"), ("EQ", "Equity"), ("LI", "Liabilities"),], max_length=11,
                    ),
                ),
                ("description", models.TextField(blank=True, max_length=1000, null=True),),
            ],
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID",),),
                (
                    "status",
                    models.CharField(
                        choices=[("PE", "Pending"), ("PY", "Paid"), ("CA", "Canceled"), ("ST", "Storno"),],
                        default="PE",
                        max_length=10,
                    ),
                ),
                ("amount", models.CharField(max_length=10)),
                ("pay_till", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID",),),
                ("amount", models.CharField(max_length=9)),
                ("pay_date", models.DateField(blank=True, null=True)),
                (
                    "methode",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("BT", "Bank"),
                            ("TW", "Twint"),
                            ("PP", "PayPal"),
                            ("CS", "Cash"),
                            ("CR", "Credit Card"),
                            ("UN", "Unclasified"),
                        ],
                        default="UN",
                        max_length=15,
                        null=True,
                    ),
                ),
                ("degistered_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID",),),
                ("translation_amount", models.CharField(max_length=10)),
                ("transaction_date", models.DateTimeField(auto_now_add=True)),
                ("account", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="accounting.Account",),),
                (
                    "invoice",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="accounting.Invoice",
                    ),
                ),
                ("payment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="accounting.Payment",),),
            ],
        ),
        migrations.CreateModel(
            name="Partner",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID",),),
                ("name", models.CharField(max_length=50)),
                ("email", models.CharField(blank=True, max_length=50, null=True),),
                ("phone", models.CharField(blank=True, max_length=50, null=True),),
                (
                    "prefered_pay",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("BT", "Bank"),
                            ("TW", "Twint"),
                            ("PP", "PayPal"),
                            ("CS", "Cash"),
                            ("CR", "Credit Card"),
                            ("UN", "Unclasified"),
                        ],
                        max_length=15,
                        null=True,
                    ),
                ),
                ("description_pay", models.TextField(blank=True, max_length=15, null=True),),
                ("account", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="accounting.Account",),),
            ],
        ),
    ]
