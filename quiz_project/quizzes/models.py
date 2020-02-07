"""Quiz model"""
from django.db import models, IntegrityError
from django.utils import timezone

from users.models import CustomUser


class Quiz(models.Model):
    """
    Quiz class, extends base Django model
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField()

    class Meta:
        db_table = 'tbl_quizzes'

    @staticmethod
    def create(name, user_id):
        """
        Creates quiz instance and tries to add it into database.
        Returns:
            quiz instance if added successfully,
            None otherwise.
        """
        quiz = Quiz(user_id=user_id, name=name, date=timezone.now())
        try:
            quiz.save()
            return quiz
        except IntegrityError:
            return None

    @staticmethod
    def is_available(name):
        """Returns whether quiz name is available"""
        return bool(Quiz.objects.get(name=name))
