# Generated by Django 4.0.3 on 2022-04-21 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0005_remove_profile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
    ]
