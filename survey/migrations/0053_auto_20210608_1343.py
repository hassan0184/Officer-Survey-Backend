# Generated by Django 3.0.7 on 2021-06-08 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0052_auto_20210607_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresponse',
            name='comment_reason',
            field=models.CharField(blank=True, max_length=800),
        ),
    ]