# Generated by Django 3.0.7 on 2020-06-19 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=100)),
                ('show_comment_box', models.BooleanField(default=False)),
                ('comment_box_place_holder', models.CharField(max_length=100)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Question')),
            ],
        ),
    ]
