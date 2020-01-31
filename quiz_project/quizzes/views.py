from functools import reduce

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect

from answers.models import Answer
from questions.models import Question
from quizRates.models import QuizRate
from quizzes.models import Quiz
from django.http import HttpResponse, HttpResponseRedirect

from scores.models import Score


def get_all_quizzes(request):
    quizzes = Quiz.objects.all()
    for quiz in quizzes:
        quiz = add_additional_info(quiz, request.user.id)
    return render(request, 'quizzes.html', {'all_quizzes': quizzes})


def get_quizzes_to_pass(request):

    return render(request, 'quizzes.html', {'all_quizzes': Quiz.objects.exclude(Quiz.passed_by_user(request.user.id))})


def calculate_score(request, questions):
    quiz_score = 0
    for question in questions:
        user_answers = [{f"{answer.id}": bool(request.POST.get(f"checkbox_answer_{answer.id}"))}
                        for answer in question.answers]
        question_result = 0
        for answer in user_answers:
            question_result += 1 if Answer.is_correct_answer(answer) else 0
        quiz_score += question_result/len(question.answers)*question.points
    return round(quiz_score, 2)


@login_required(login_url='/users/login/')
def pass_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz_id=quiz.id).order_by('id')
    for question in questions:
        question.answers = Answer.objects.filter(question_id=question.id).order_by('id')
    if request.method == "GET":
        return render(request, 'pass_quiz.html', {'quiz': quiz,
                                                  'questions': questions})
    quiz_score = calculate_score(request, questions)
    best_score = Score.get_score(quiz.id, request.user.id)
    score = Score(user_id=request.user.id, quiz_id=quiz_id, score=quiz_score)
    if best_score == -1:
        score.save()
    else:
        score = Score.objects.get(user_id=request.user.id, quiz_id=quiz_id)
        score.score = best_score if best_score >= quiz_score else quiz_score
        score.save()
    request.session['_old_post'] = {"score": quiz_score, 'quiz_name': quiz.name, "best_score": best_score}
    return HttpResponseRedirect(f'/quizzes/{quiz.id}/result')


@login_required(login_url='/users/login/')
def quiz_result(request, quiz_id):
    score, quiz_name, best_score = list(request.session.get('_old_post').values())
    quiz_rate = QuizRate.get_quiz_rate(quiz_id, request.user.id)
    if request.method == "GET":
        return render(request, 'quiz_result.html', {'score': score,
                                                    'quiz_name': quiz_name,
                                                    'quiz_id': quiz_id,
                                                    'best_score': best_score,
                                                    'rate': int(quiz_rate.rate) if quiz_rate else 0,
                                                    'comment': str(quiz_rate.comment) if quiz_rate else ""})
    rate = request.POST.get('checkbox_rate') if request.POST.get('checkbox_rate') else 0
    comment = str(request.POST.get('comment'))
    if quiz_rate:
        quiz_rate.rate = rate
        quiz_rate.comment = comment
        quiz_rate.save()
    else:
        QuizRate(user_id=request.user.id, quiz_id=quiz_id, rate=rate, comment=comment).save()
    return redirect('homepage')


@login_required(login_url='/users/login/')
def create_quiz(request):
    if request.method == "GET":
        return render(request, 'add_questions2.html', {'quiz': Quiz(name="testttt", user_id=request.user.id),
                                                      'questions_count': 1,
                                                      'range_questions_count': range(1),
                                                      'answers_count': 2,
                                                      'range_answers_count': range(2)})
    quiz_name = request.POST.get('quiz_name')
    questions_count = int(request.POST.get('questions_count'))
    answers_count = int(request.POST.get('answers_count'))
    quiz = Quiz.create(name=quiz_name, user_id=request.user.id)
    if quiz:
        return render(request, 'add_questions2.html', {'quiz': quiz,
                                                      'questions_count': questions_count,
                                                      'range_questions_count': range(questions_count),
                                                      'answers_count': answers_count,
                                                      'range_answers_count': range(answers_count)}, )
    return redirect('create_quiz')


def add_additional_info(quiz, user_id):
    rates = QuizRate.objects.filter(quiz_id=quiz.id)
    questions = Question.objects.filter(quiz_id=quiz.id)
    quiz.rate = rates.aggregate(Sum('rate'))['rate__sum'] if rates else 0
    quiz.comment = list(rates.order_by('-id'))[0].comment if rates else "There is no comments for this quiz yet("
    quiz.questions_count = len(questions)
    quiz.best_score = Score.get_score(quiz.id, user_id)
    quiz.max_points = questions.aggregate(Sum('points'))['points__sum'] if questions else 0
    return quiz
