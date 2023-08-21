# Generated by Django 3.0.7 on 2020-10-28 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20201028_0750'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('officer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Officer')),
            ],
        ),
    ]