# Generated by Django 3.0.7 on 2020-09-23 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20200814_0646'),
        ('department', '0015_support'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Officer'),
        ),
    ]
