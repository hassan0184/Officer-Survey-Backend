# Generated by Django 3.0.7 on 2020-06-21 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200621_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supervisor',
            name='profile_pic',
            field=models.ImageField(default='default_profie_pic.png', upload_to=''),
        ),
    ]
