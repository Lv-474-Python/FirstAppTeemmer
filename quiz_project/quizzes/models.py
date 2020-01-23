from django.db import models

from users.models import CustomUser


class Quiz(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateTimeField()

    class Meta:
        db_table = 'tbl_quizzes'
