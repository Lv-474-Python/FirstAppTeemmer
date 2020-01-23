from django.db import models
from quizzes.models import Quiz


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    points = models.IntegerField(default=1)

    class Meta:
        db_table = 'tbl_questions'
