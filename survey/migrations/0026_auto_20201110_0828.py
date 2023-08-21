# Generated by Django 3.0.7 on 2020-11-10 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_auto_20201110_0824'),
        ('survey', '0025_auto_20201104_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresponse',
            name='reviewed_by_supervisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_by_supervisor', to='accounts.Officer'),
        ),
        migrations.AlterField(
            model_name='surveyresponse',
            name='officer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveyed_officer', to='accounts.Officer'),
        ),
    ]