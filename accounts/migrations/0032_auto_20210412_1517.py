# Generated by Django 3.0.7 on 2021-04-12 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20210301_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='profilePicture/default_profie_pic.png', upload_to='profilePicture'),
        ),
    ]