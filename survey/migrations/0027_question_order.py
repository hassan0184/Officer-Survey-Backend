# Generated by Django 3.0.7 on 2020-11-16 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0026_auto_20201110_0828'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
