# Generated by Django 3.0.7 on 2021-04-27 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0044_auto_20210424_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee360questionresponse',
            name='file',
            field=models.FileField(null=True, upload_to='employee360Files'),
        ),
        migrations.AlterField(
            model_name='employee360questionresponse',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
