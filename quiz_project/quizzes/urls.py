from django.urls import path, include

from . import views

urlpatterns = [
    path('<int:q_id>/', include('questions.urls')),
    path('create', views.create_quiz, name='create_quiz'),
    path('', views.get_all_quizzes, name='get_all_quizzes'),
]
