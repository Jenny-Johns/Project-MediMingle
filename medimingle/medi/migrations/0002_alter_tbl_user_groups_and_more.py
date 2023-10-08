# Generated by Django 4.2.5 on 2023-10-06 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('medi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='custom_users', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='tbl_user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='custom_users_permissions', to='auth.permission'),
        ),
    ]
