# Generated by Django 4.2.5 on 2024-05-09 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medi', '0009_doctorrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_time_slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='medi.appointmenttime'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_image',
            field=models.ImageField(default='default.png', upload_to='doctor/'),
        ),
    ]
