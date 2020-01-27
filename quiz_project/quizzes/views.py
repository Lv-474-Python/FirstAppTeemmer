from functools import reduce

from django.shortcuts import render, redirect

from answers.models import Answer
from questions.models import Question
from quizzes.models import Quiz
from django.http import HttpResponse

from scores.models import Score


def get_all_quizzes(request):
    return render(request, 'quizzes.html', {'all_quizzes': Quiz.objects.all()})


def get_quizzes_to_pass(request):

    return render(request, 'quizzes.html', {'all_quizzes': Quiz.objects.exclude(Quiz.passed_by_user(request.user.id))})


def pass_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz_id=quiz.id).order_by('id')
    for question in questions:
        question.answers = Answer.objects.filter(question_id=question.id).order_by('id')
    if request.method == "GET":
        return render(request, 'pass_quiz.html', {'quiz': quiz,
                                                  'questions': questions})
    quiz_result = 0
    for question in questions:
        user_answers = [{f"{answer.id}": bool(request.POST.get(f"checkbox_answer_{answer.id}"))}
                        for answer in question.answers]
        question_result = 0
        for answer in user_answers:
            question_result += 1 if Answer.is_correct_answer(answer) else 0
        quiz_result += question_result/len(question.answers)*question.points
    quiz_result = round(quiz_result, 2)
    best_score = Score.get_score(quiz.id, request.user.id)
    score = Score(user_id=request.user.id, quiz_id=quiz_id, score=quiz_result)
    if best_score == -1:
        score.save()
    else:
        score = Score.objects.get(user_id=request.user.id, quiz_id=quiz_id)
        score.score = best_score if best_score >= quiz_result else quiz_result
        score.save()
    return render(request, 'quiz_result.html', {'score': quiz_result,
                                                'quiz': quiz,
                                                'best_score': best_score})


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
