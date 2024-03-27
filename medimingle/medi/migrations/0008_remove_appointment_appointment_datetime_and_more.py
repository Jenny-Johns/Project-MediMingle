# Generated by Django 4.2.5 on 2024-03-22 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medi', '0007_alter_appointment_appointment_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_datetime',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_time_slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='medi.appointmenttime'),
        ),
    ]
