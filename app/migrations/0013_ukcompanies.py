# Generated by Django 4.2.6 on 2024-04-25 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_companies'),
    ]

    operations = [
        migrations.CreateModel(
            name='UkCompanies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('country', models.CharField(max_length=1000)),
                ('linkedin_profile_link', models.CharField(max_length=1000)),
            ],
        ),
    ]