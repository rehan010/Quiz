# Generated by Django 2.2.14 on 2022-01-15 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0015_userquiz_insrtctions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userquiz',
            name='file_share_path',
        ),
    ]
