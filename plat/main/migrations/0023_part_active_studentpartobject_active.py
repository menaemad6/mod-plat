# Generated by Django 4.1.7 on 2023-10-16 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_part_views_limit_studentpartobject_views_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentpartobject',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]