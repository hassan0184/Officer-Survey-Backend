# Generated by Django 3.0.7 on 2022-03-24 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0062_auto_20220322_1242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smssurvey',
            old_name='event_type',
            new_name='eventtype',
        ),
    ]