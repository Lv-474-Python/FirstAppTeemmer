from django.db import models
from questions.models import Question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'tbl_answers'
