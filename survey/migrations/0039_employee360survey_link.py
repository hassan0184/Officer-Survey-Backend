# Generated by Django 3.0.7 on 2021-04-13 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0038_employee360choice_employee360question_employee360survey'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee360survey',
            name='link',
            field=models.CharField(default=1, editable=False, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
