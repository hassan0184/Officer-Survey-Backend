# Generated by Django 3.0.7 on 2020-06-21 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20200621_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default_profie_pic.png', null=True, upload_to=''),
        ),
    ]