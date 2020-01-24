from django.shortcuts import render, redirect

from answers.models import Answer
from questions.models import Question
from answers.views import get_answers


def get_question(request, q_id, question_id):
    return render(request, 'questions.html', {'question': Question.objects.filter(id=question_id)
                                              , 'answers': get_answers(question_id)})


def get_all_questions(request, q_id):
    return render(request, 'questions.html', {'all_questions': Question.objects.filter(quiz_id=q_id)})


def add(request):
    questions_count = int(request.POST.get('questions_count'))
    answers_count = int(request.POST.get('answers_count'))
    quiz_id = int(request.POST.get('quiz_id'))
    for i in range(questions_count):
        question = Question.create(text=request.POST.get(f'question_{i}'), quiz_id=quiz_id)
        question_id = question.id
        for j in range(answers_count):
            Answer.create(question_id=question_id, text=request.POST.get(f'answer_{i}_{j}'),
                          is_correct=bool(request.POST.get(f'is_correct_{i}_{j}')))
    return redirect('homepage')

