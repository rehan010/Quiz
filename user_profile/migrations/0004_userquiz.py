# Generated by Django 2.2.14 on 2021-12-25 07:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0003_auto_20180318_0741'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_artifact', models.IntegerField(blank=True, default=5, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('artifact_name', models.CharField(editable=False, max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_quiz', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
