from django.shortcuts import render
from questions.models import Question
from answers.views import get_answers


def get_question(request, q_id, question_id):
    return render(request, 'questions.html', {'question': Question.objects.filter(id=question_id)
                                              , 'answers': get_answers(question_id)})


def get_all_questions(request, q_id):
    return render(request, 'questions.html', {'all_questions': Question.objects.filter(quiz_id=q_id)})


