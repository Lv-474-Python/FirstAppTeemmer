# Generated by Django 3.0.2 on 2020-01-28 16:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizzes', '0001_initial'),
        ('quizRates', '0002_auto_20200128_1620'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='quizrate',
            unique_together={('user', 'quiz')},
        ),
    ]