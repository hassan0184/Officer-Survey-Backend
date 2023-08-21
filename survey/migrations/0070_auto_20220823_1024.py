# Generated by Django 3.0.7 on 2022-08-23 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0069_auto_20220810_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitysurvey',
            name='survery_category',
            field=models.CharField(choices=[('Citizen_Police_Academy', 'Citizen Police Academy Survey'), ('Community_Engagement', 'Community Engagement Survey'), ('Crime', 'Crime Survey'), ('Police_Public_Contact', 'Police Public Contract Survey'), ('Public_Safety', 'Public Safety Survey'), ('Community_Pulse', 'Community Pulse Survey'), ('Resident_Statisfaction', 'Resident Statisfaction Survey'), ('Small_Buisness', 'Small Business Survey'), ('School_Safety', 'School Safety Survey'), ('Everything', 'Everything Else')], default='Everything', max_length=50),
        ),
    ]
