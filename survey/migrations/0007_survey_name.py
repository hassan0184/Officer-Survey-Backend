# Generated by Django 3.0.7 on 2020-06-21 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_delete_departmentsurvey'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='name',
            field=models.CharField(default='Sample Survey', max_length=100),
        ),
    ]
