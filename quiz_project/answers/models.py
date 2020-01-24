from django.db import models, IntegrityError
from questions.models import Question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'tbl_answers'

    @staticmethod
    def create(text, is_correct, question_id):
        answer = Answer(question_id=question_id, text=text, is_correct=is_correct)
        try:
            answer.save()
            return answer
        except IntegrityError:
            return None
