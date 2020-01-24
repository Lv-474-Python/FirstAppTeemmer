from django.shortcuts import render, redirect
from quizzes.models import Quiz
from django.http import HttpResponse


def get_all_quizzes(request):
    return render(request, 'quizzes.html', {'all_quizzes': Quiz.objects.all()})


def create_quiz(request):
    if request.method == "GET":
        return render(request, 'create_quiz.html')
    quiz_name = request.POST.get('quiz_name')
    questions_count = int(request.POST.get('questions_count'))
    answers_count = int(request.POST.get('answers_count'))
    quiz = Quiz.create(name=quiz_name, user_id=request.user.id)
    if quiz:
        return render(request, 'add_questions.html', {'quiz': quiz,
                                                      'questions_count': questions_count,
                                                      'range_questions_count': range(questions_count),
                                                      'answers_count': answers_count,
                                                      'range_answers_count': range(answers_count)}, )
    return redirect('create_quiz')
