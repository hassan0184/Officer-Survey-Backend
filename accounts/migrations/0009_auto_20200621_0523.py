# Generated by Django 3.0.7 on 2020-06-21 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200621_0457'),
    ]

    operations = [
        migrations.RenameField(
            model_name='officer',
            old_name='batch_id',
            new_name='badge_number',
        ),
    ]