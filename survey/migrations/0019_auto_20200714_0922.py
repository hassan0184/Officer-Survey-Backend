# Generated by Django 3.0.7 on 2020-07-14 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0018_auto_20200705_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresponse',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
