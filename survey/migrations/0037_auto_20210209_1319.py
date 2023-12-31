# Generated by Django 3.0.7 on 2021-02-09 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0036_auto_20210114_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicetranslation',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('ar', 'Arabic'), ('ko', 'Korean'), ('zh-CN', 'Chinese (Simplified)')], default='English', max_length=100),
        ),
        migrations.AlterField(
            model_name='questiontranslation',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('ar', 'Arabic'), ('ko', 'Korean'), ('zh-CN', 'Chinese (Simplified)')], default='English', max_length=100),
        ),
    ]
