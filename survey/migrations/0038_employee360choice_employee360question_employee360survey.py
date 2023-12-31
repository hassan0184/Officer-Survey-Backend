# Generated by Django 3.0.7 on 2021-04-12 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0024_auto_20210412_1517'),
        ('survey', '0037_auto_20210209_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee360Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sample 360 Employee Survey', max_length=100)),
                ('instruction', models.TextField(max_length=500)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Employee360Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('Multiple Choice', 'Multiple Choice'), ('Drop Down', 'Drop Down'), ('Text Area', 'Text Area')], default='Mutiple Choice', max_length=100)),
                ('order', models.IntegerField(default=0)),
                ('required', models.BooleanField(default=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='survey.Employee360Survey')),
            ],
        ),
        migrations.CreateModel(
            name='Employee360Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=100)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='survey.Employee360Question')),
            ],
        ),
    ]
