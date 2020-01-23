from django.urls import path, include

from . import views

urlpatterns = [
    path('questions/<int:question_id>/', views.get_question, name='get_question'),
    path('questions', views.get_all_questions, name='get_all_questions')
]