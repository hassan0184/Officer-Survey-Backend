# Generated by Django 3.0.7 on 2020-06-21 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_delete_departmentsurvey'),
        ('department', '0003_auto_20200621_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='survey.Survey'),
        ),
    ]
