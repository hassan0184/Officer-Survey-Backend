# Generated by Django 3.0.7 on 2020-10-28 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_log'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='training',
            new_name='in_training',
        ),
    ]
