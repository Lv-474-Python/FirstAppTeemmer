from django.urls import path, include

from .views import create_quiz, get_all_quizzes, pass_quiz

urlpatterns = [
    path('<int:quiz_id>/', pass_quiz, name='pass_quiz'),
    path('create', create_quiz, name='create_quiz'),
    path('', get_all_quizzes, name='get_all_quizzes'),
]
