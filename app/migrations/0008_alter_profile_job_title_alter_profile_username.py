# Generated by Django 4.2.6 on 2024-04-16 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='job_title',
            field=models.CharField(default=None, max_length=5000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(default=None, max_length=1000),
        ),
    ]
