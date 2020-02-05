from django.db import models
from django.db.models import Sum

from users.models import CustomUser
from quizzes.models import Quiz


class QuizRate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.CharField(max_length=250)

    class Meta:
        db_table = 'tbl_quiz_rates'
        unique_together = [
            ("user", "quiz"),
        ]

    @staticmethod
    def get_users_rate(quiz_id, user_id):
        rate = QuizRate.objects.filter(user_id=user_id, quiz_id=quiz_id)
        if rate:
            return rate[0]
        return None

    @staticmethod
    def get_rate(quiz_id):
        rate = QuizRate.objects.filter(quiz_id=quiz_id).aggregate(Sum('rate'))['rate__sum']
        if rate:
            return rate
        return 0
