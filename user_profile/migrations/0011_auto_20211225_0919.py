# Generated by Django 2.2.14 on 2021-12-25 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0010_auto_20211225_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquiz',
            name='bg_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
