from django.db import models
from users.models import CustomUser
from quizzes.models import Quiz


class QuizRate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.CharField(max_length=250)

    class Meta:
        db_table = 'tbl_quiz_rates'
