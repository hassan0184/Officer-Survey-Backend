# Generated by Django 3.0.7 on 2021-06-29 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0025_auto_20210423_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='is_suspend',
            field=models.BooleanField(default=False),
        ),
    ]
