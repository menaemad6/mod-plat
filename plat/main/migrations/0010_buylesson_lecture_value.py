# Generated by Django 4.1.7 on 2023-10-11 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_logininfo_username_alter_logininfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='buylesson',
            name='lecture_value',
            field=models.IntegerField(blank=True, default='0'),
        ),
    ]
