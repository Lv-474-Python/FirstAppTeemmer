from django.urls import path, include

from .views import get_question, get_all_questions, add

urlpatterns = [
    path('questions/<int:question_id>/', get_question, name='get_question'),
    path('questions', get_all_questions, name='get_all_questions'),
    path('add', add, name='add'),
]
