# Generated by Django 2.2.14 on 2021-12-25 08:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_auto_20211225_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquiz',
            name='bg_transparency',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]