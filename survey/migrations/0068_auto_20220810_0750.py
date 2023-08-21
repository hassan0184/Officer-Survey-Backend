# Generated by Django 3.0.7 on 2022-08-10 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0067_auto_20220802_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitysurvey',
            name='survery_category',
            field=models.CharField(choices=[('Recuirment Surveys', 'Recuirment Survey'), ('Pre-Employment Surveys', 'Pre Employment Survey'), ('Onboarding Surveys', 'Onboarding Survey'), ('Traning Surveys', 'Traning Survey'), ('Pulse Surveys', 'Pulse Survey'), ('Employee Satisfaction Surveys', 'Employee Satisfaction Survey'), ('Organizational Surveys', 'Organizational Survey'), ('Exit Surveys', 'Exit Survey'), ('Everything Else Surveys', 'Everything Else')], default='Everything Else Surveys', max_length=50),
        ),
    ]
