# Generated by Django 3.0.2 on 2020-01-27 15:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizzes', '0001_initial'),
        ('scores', '0001_initial'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='score',
            index_together={('user', 'quiz')},
        ),
    ]
