from functools import reduce

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.shortcuts import render, redirect

from answers.models import Answer
from questions.models import Question
from quizRates.models import QuizRate
from quizzes.models import Quiz
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from scores.models import Score
from users.models import CustomUser


@login_required
def get_all_quizzes(request):
    search = ""
    if request.method == "POST":
        search = request.POST.get('search_by_name').strip()
    if search:
        quizzes = Quiz.objects.filter(name__contains=search).order_by('-id')
    else:
        quizzes = Quiz.objects.all().order_by('-id')
    for quiz in quizzes:
        add_additional_info(quiz, request.user.id)
    return render(request, 'quizzes.html', {'all_quizzes': quizzes,
                                            'search_value': search})


def calculate_score(request, questions):
    quiz_score = 0
    for question in questions:
        user_answers = [{f"{answer.id}": bool(request.POST.get(f"checkbox_answer_{answer.id}"))}
                        for answer in question.answers]
        question_result = 0
        for answer in user_answers:
            question_result += Answer.is_correct_answer(answer)
        quiz_score += question_result/len(question.answers)*question.points
    return round(quiz_score, 2)


@login_required
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
    if best_score != -1:
        score = Score.objects.get(user_id=request.user.id, quiz_id=quiz_id)
        score.score = best_score if best_score >= quiz_score else quiz_score
    score.save()
    request.session['_old_post'] = {"score": quiz_score, 'quiz_name': quiz.name, "best_score": best_score}
    return HttpResponseRedirect(f'/quizzes/{quiz.id}/result')


@login_required
def quiz_result(request, quiz_id):
    score, quiz_name, best_score = list(request.session.get('_old_post').values())
    quiz_rate = QuizRate.get_users_rate(quiz_id, request.user.id)
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


@login_required
def create_quiz(request):
    if request.method == "GET":
        return render(request, 'create_quiz.html')
    quiz_name = request.POST.get('quiz_name')
    q_num = 1
    quiz = Quiz.create(name=quiz_name, user_id=request.user.id)
    while quiz and str(request.POST.get('question_' + str(q_num))) != 'None':
        q_text = str(request.POST.get('question_' + str(q_num)))
        points = int(request.POST.get('question_pts_' + str(q_num)))
        question = Question.create(q_text, quiz.id, points)
        a_num = 1
        while question and str(request.POST.get('answer_' + str(q_num) + '_' + str(a_num))) != 'None':
            answer = str(request.POST.get('answer_' + str(q_num) + '_' + str(a_num)))
            is_correct = bool(request.POST.get('is_correct_' + str(q_num) + '_' + str(a_num)))
            Answer.create(answer, is_correct, question.id)
            a_num += 1
        q_num += 1
    if quiz:
        return redirect('homepage')
    return redirect('create_quiz')


def add_additional_info(quiz, user_id):
    rates = QuizRate.objects.filter(quiz_id=quiz.id)
    questions = Question.objects.filter(quiz_id=quiz.id)
    quiz.rate = QuizRate.get_rate(quiz.id)
    quiz.users_passed = len(Score.objects.filter(quiz_id=quiz.id))
    quiz.comment = list(rates.order_by('-id'))[0].comment if rates else ""
    quiz.questions_count = len(questions)
    quiz.best_score = Score.get_score(quiz.id, user_id)
    quiz.max_points = questions.aggregate(Sum('points'))['points__sum'] if questions else 0
    quiz.creator_name = CustomUser.objects.get(id=quiz.user_id).username
    return quiz


@login_required
def check_quiz_name(request, quiz_name):
    if Quiz.objects.filter(name=quiz_name):
        return JsonResponse({'available': False})
    return JsonResponse({'available': True})


def get_users_quizzes(request):
    quizzes = []
    for quiz in Quiz.objects.filter(user_id=request.user.id).order_by('-id'):
        quizzes.append({'passed_count': len(Score.objects.filter(quiz_id=quiz.id)),
                        'rate': QuizRate.get_rate(quiz.id),
                        'avg_score': Score.get_avg_score(quiz.id),
                        'id': quiz.id,
                        'date': quiz.date,
                        'name': quiz.name})
    return JsonResponse({'quizzes': quizzes})


@login_required
def get_passed_quizzes(request):
    scores = Score.objects.filter(user_id=request.user.id)
    quizzes = [quiz for quiz in Quiz.objects.all().order_by('-id') if Score.get_score(quiz.id, request.user.id) != -1]
    result = []
    for quiz in quizzes:
        result.append({'user_score': str(Score.get_score(quiz.id, request.user.id)),
                       'rate': QuizRate.get_rate(quiz.id),
                       'avg_score': Score.get_avg_score(quiz.id),
                       'id': quiz.id,
                       'date': quiz.date,
                       'name': quiz.name})
    return JsonResponse({'quizzes': result})


@login_required
def get_quizzes_to_pass(request):
    scores = Score.objects.filter(user_id=request.user.id)
    search = ""
    if request.method == "POST":
        search = request.POST.get('search_by_name').strip()
    if search:
        quizzes = Quiz.objects.filter(name__contains=search).order_by('-id')
    else:
        quizzes = Quiz.objects.all().order_by('-id')
    for score in scores:
        quizzes = quizzes.exclude(id=score.quiz_id)
    for quiz in quizzes:
        add_additional_info(quiz, request.user.id)
    return render(request, 'quizzes.html', {'all_quizzes': quizzes,
                                            'search_value': search,
                                            'np': True})


def quiz_comments(request, quiz_id):
    rates = QuizRate.objects.filter(quiz_id=quiz_id)
    return render(request, 'quiz_comments.html', {'rates': rates})

