# Generated by Django 4.1.7 on 2023-10-17 20:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_alter_buylesson_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='studentpartobject',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
