# Generated by Django 4.0.3 on 2023-03-11 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_album_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=62),
        ),
    ]
