from django.db import models, IntegrityError
from django.utils import timezone

from users.models import CustomUser


class Quiz(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField()

    class Meta:
        db_table = 'tbl_quizzes'

    @staticmethod
    def create(name, user_id):
        quiz = Quiz(user_id=user_id, name=name, date=timezone.now())
        try:
            quiz.save()
            return quiz
        except IntegrityError:
            return None

    @staticmethod
    def is_available(name):
        return False if Quiz.objects.get(name=name) else True

