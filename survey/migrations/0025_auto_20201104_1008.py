# Generated by Django 3.0.7 on 2020-11-04 10:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0024_auto_20201103_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresponse',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
