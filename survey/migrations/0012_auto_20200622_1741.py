# Generated by Django 3.0.7 on 2020-06-22 17:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0011_auto_20200622_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresponse',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surveyresponse',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]