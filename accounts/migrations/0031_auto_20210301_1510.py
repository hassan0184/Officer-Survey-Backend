# Generated by Django 3.0.7 on 2021-03-01 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_notes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notes',
            old_name='notes_By',
            new_name='notes_by',
        ),
    ]
