# Generated by Django 4.2.5 on 2023-12-05 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medi', '0006_alter_doctor_consulting_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='consulting_fee',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='patientappointment',
            name='appoint_date',
            field=models.DateField(max_length=50, null=True),
        ),
    ]
