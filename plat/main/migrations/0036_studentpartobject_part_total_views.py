# Generated by Django 4.1.7 on 2023-10-22 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_studentlectureobject_parts_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentpartobject',
            name='part_total_views',
            field=models.IntegerField(default=0),
        ),
    ]
