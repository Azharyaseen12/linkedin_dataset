# Generated by Django 4.2.6 on 2024-04-16 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_profile_job_title_alter_profile_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]