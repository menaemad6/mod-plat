# Generated by Django 4.1.7 on 2023-10-16 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_lecture_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='part',
            name='youtube_url',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='studentpartobject',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentpartobject',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='studentpartobject',
            name='youtube_url',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
