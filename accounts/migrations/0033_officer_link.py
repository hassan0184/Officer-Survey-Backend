# Generated by Django 3.0.7 on 2022-08-12 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_auto_20210412_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='officer',
            name='link',
            field=models.CharField(blank=True, editable=False, max_length=10, null=True, unique=True),
        ),
    ]
