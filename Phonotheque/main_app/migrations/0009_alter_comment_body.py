# Generated by Django 4.0.3 on 2022-04-03 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_comment_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.CharField(max_length=620),
        ),
    ]
