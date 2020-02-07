"""Scores model"""
from django.db import models
from django.db.models import Avg

from users.models import CustomUser
from quizzes.models import Quiz


class Score(models.Model):
    """
    Score class, extends base Django model
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()

    class Meta:
        db_table = 'tbl_scores'
        unique_together = [
            ("user", "quiz"),
        ]

    @staticmethod
    def get_score(quiz_id, user_id):
        """
        gets score value from database.
        Returns:
            score value if found, -1 otherwise.
        """
        score = Score.objects.filter(user_id=user_id, quiz_id=quiz_id)
        if score:
            return float(score[0].score)
        return -1

    @staticmethod
    def get_avg_score(quiz_id):
        """
        calculates average score from database.
        Returns:
            average score if there any scores for this quiz,
            0 otherwise.
        """
        score = Score.objects.filter(quiz_id=quiz_id)
        if score:
            return round(score.aggregate(Avg('score'))['score__avg'], 2)
        return 0
