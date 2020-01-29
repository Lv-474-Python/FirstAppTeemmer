from django.urls import path, include

from .views import create_quiz, get_all_quizzes, pass_quiz, quiz_result

urlpatterns = [
    path('<int:quiz_id>/', pass_quiz, name='pass_quiz'),
    path('<int:quiz_id>/result/', quiz_result, name='quiz_result'),
    path('create', create_quiz, name='create_quiz'),
    path('', get_all_quizzes, name='get_all_quizzes'),
]
