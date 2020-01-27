from django.db import models
from users.models import CustomUser
from quizzes.models import Quiz


class Score(models.Model):
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
        score = Score.objects.filter(user_id=user_id, quiz_id=quiz_id)
        if score:
            return float(score[0].score)
        return -1
