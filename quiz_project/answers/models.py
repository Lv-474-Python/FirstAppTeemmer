"""answer model"""
from django.db import models, IntegrityError
from questions.models import Question


class Answer(models.Model):
    """
    Answer class, extends base Django model
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'tbl_answers'

    @staticmethod
    def create(text, is_correct, question_id):
        """
        Creates answer instance and tries to add it into database.
        Returns:
            answer instance if added successfully,
            None otherwise.
        """
        answer = Answer(question_id=question_id, text=text, is_correct=is_correct)
        try:
            answer.save()
            return answer
        except IntegrityError:
            return None

    @staticmethod
    def is_correct_answer(answer):
        """
            Returns True if user's answer matches with answer from database.
        """
        db_answer = Answer.objects.get(id=int(list(answer.keys())[0]))
        return db_answer.is_correct == bool(list(answer.values())[0])
