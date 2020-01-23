from django.shortcuts import render
from answers.models import Answer


def get_answers(q_id):
    return Answer.objects.filter(question_id=q_id)
