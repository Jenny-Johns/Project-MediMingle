# Generated by Django 4.2.5 on 2024-04-17 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalhistory',
            name='age',
        ),
        migrations.RemoveField(
            model_name='medicalhistory',
            name='blood_group',
        ),
    ]
