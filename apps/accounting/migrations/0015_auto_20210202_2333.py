# Generated by Django 2.2.17 on 2021-02-02 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0014_creditnote_creditnotedate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creditnote',
            old_name='credited_date',
            new_name='credit_date',
        ),
        migrations.RenameField(
            model_name='creditnote',
            old_name='credit',
            new_name='credited',
        ),
    ]
