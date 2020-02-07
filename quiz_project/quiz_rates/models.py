"""QuizRate model"""
from django.db import models
from django.db.models import Sum

from users.models import CustomUser
from quizzes.models import Quiz


class QuizRate(models.Model):
    """
    QuizRate class, extends base Django model
    """
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
        """
            returns QuizRate object if found, None otherwise
        """
        rate = QuizRate.objects.filter(user_id=user_id, quiz_id=quiz_id)
        if rate:
            return rate[0]
        return None

    @staticmethod
    def get_rate(quiz_id):
        """
            rate for a quiz = Sum of all rates for this quiz.
            Returns rate if any in database, 0 otherwise.
        """
        rate = QuizRate.objects.filter(quiz_id=quiz_id).aggregate(Sum('rate'))['rate__sum']
        if rate:
            return rate
        return 0

    @staticmethod
    def get_last_comment(quiz_id):
        """
            returns last non-empty string comment for a quiz.
        """
        comments = [qr.comment for qr in QuizRate.objects.filter(quiz_id=quiz_id).order_by('-id')]
        for comment in comments:
            if comment:
                return comment
        return "No comments yet"
