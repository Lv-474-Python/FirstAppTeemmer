from django.shortcuts import render
from quizzes.models import Quiz
from django.http import HttpResponse


def get_all_quizzes(request):
    return render(request, 'quizzes.html', {'all_quizzes': Quiz.objects.all()})


def create_quiz(request):
    return render(request, 'create_quiz.html')
