# Generated by Django 4.2.5 on 2024-04-02 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medi', '0008_remove_appointment_appointment_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointment_datetime',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_time',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
