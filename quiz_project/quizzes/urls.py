from django.urls import path, include

from .views import (create_quiz,
                    get_all_quizzes,
                    pass_quiz,
                    quiz_result,
                    check_quiz_name,
                    get_passed_quizzes,
                    get_users_quizzes,
                    quiz_comments,
                    get_quizzes_to_pass,
                    )

urlpatterns = [
    path('<int:quiz_id>/', pass_quiz, name='pass_quiz'),
    path('<int:quiz_id>/result/', quiz_result, name='quiz_result'),
    path('<int:quiz_id>/comments/', quiz_comments, name='quiz_comments'),
    path('create', create_quiz, name='create_quiz'),
    path('all', get_all_quizzes, name='get_all_quizzes'),
    path('not_passed', get_quizzes_to_pass, name='get_quizzes_to_pass'),
    path('get_passed/', get_passed_quizzes, name='get_passed_quizzes'),
    path('get_users/', get_users_quizzes, name='get_users_quizzes'),
    path('check/<str:quiz_name>', check_quiz_name, name='check_quiz_name'),
]
