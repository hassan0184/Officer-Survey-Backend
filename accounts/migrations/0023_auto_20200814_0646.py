# Generated by Django 3.0.7 on 2020-08-14 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0013_auto_20200809_0558'),
        ('accounts', '0022_officer_training'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.District'),
        ),
    ]
