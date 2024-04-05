# Generated by Django 4.1.7 on 2023-10-11 23:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=100)),
                ('password', models.CharField(blank=True, max_length=100)),
                ('device_type', models.CharField(blank=True, max_length=100)),
                ('browser_type', models.CharField(blank=True, max_length=100)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'Login Info',
                'verbose_name_plural': 'Login Infos',
            },
        ),
        migrations.DeleteModel(
            name='Info',
        ),
    ]