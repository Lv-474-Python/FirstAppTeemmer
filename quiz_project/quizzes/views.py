"""
Views for quiz model,
renders pages for quiz creation, quiz passing, results, ability to rate
and leave a comment, search quizzes.
"""
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from answers.models import Answer
from questions.models import Question
from quiz_rates.models import QuizRate
from quizzes.models import Quiz
from scores.models import Score
from users.models import CustomUser


@login_required
def get_all_quizzes(request):
    """Renders quizzes page with specific search value"""
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
    """
    Function to calculate score for a quiz.

    Returns rounded value for better view.
    """
    quiz_score = 0
    for question in questions:
        user_answers = [{f"{answer.id}": bool(request.POST.get(f"checkbox_answer_{answer.id}"))}
                        for answer in question.answers]
        question_result = 0
        for answer in user_answers:
            question_result += Answer.is_correct_answer(answer)
        quiz_score += question_result / len(question.answers) * question.points
    return round(quiz_score, 2)


@login_required
def pass_quiz(request, quiz_id):
    """
    Renders page with all questions and answers for specific quiz.
    on POST calculates users score and saves it into database if there is no data
    in database, rewrites the score if user got more points than he had before
    and redirects to results page.
    """
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
    request.session['_old_post'] = {"score": quiz_score,
                                    'quiz_name': quiz.name,
                                    "best_score": best_score}
    return HttpResponseRedirect(f'/quizzes/{quiz.id}/result')


@login_required
def quiz_result(request, quiz_id):
    """
        Renders page, where users sees his results on quiz he passed
        and where he can leave comment and rate
        Before rendering, checks whether user leaved comment before and
        passes it into page if yes so user can change it after repassing quiz.
    """
    score, quiz_name, best_score = list(request.session.get('_old_post').values())
    quiz_rate = QuizRate.get_users_rate(quiz_id, request.user.id)
    if request.method == "GET":
        return render(request,
                      'quiz_result.html',
                      {
                          'score': score,
                          'max_points': get_max_points(quiz_id),
                          'quiz_name': quiz_name,
                          'quiz_id': quiz_id,
                          'best_score': best_score,
                          'rate': int(quiz_rate.rate) if quiz_rate else 0,
                          'comment': str(quiz_rate.comment) if quiz_rate else ""
                      })
    rate = request.POST.get('checkbox_rate', 0)
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
    """
        View for quiz creation page.
        if GET method, renders quiz creation page.
        on POST, reads all the info, user entered and
        saves quiz, it questions and theirs answers.

        Redirects to homepage if created successfully,
        renders same page otherwise.
    """
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
        while question and str(request.POST.get(f'answer_{q_num}_{a_num}')) != 'None':
            answer = str(request.POST.get(f'answer_{q_num}_{a_num}'))
            is_correct = bool(request.POST.get(f'is_correct_{q_num}_{a_num}'))
            Answer.create(answer, is_correct, question.id)
            a_num += 1
        q_num += 1
    if quiz:
        return redirect('homepage')
    return redirect('create_quiz')


def add_additional_info(quiz, user_id):
    """adds additional info to quiz instance"""
    questions = Question.objects.filter(quiz_id=quiz.id)
    quiz.rate = QuizRate.get_rate(quiz.id)
    quiz.users_passed = len(Score.objects.filter(quiz_id=quiz.id))
    quiz.comment = QuizRate.get_last_comment(quiz.id)
    quiz.questions_count = len(questions)
    quiz.best_score = Score.get_score(quiz.id, user_id)
    quiz.max_points = get_max_points(quiz.id) if questions else 0
    quiz.creator_name = CustomUser.objects.get(id=quiz.user_id).username
    return quiz


@login_required
def check_quiz_name(request, quiz_name):
    """
    individual view for AJAX request from create_quiz page,
    checks, whether such quiz name is in database,
    returns proper JSON response.
    """
    if Quiz.objects.filter(name=quiz_name):
        return JsonResponse({'available': False})
    return JsonResponse({'available': True})


@login_required
def get_users_quizzes(request):
    """
        individual view for AJAX request from profile page,
        returns list of dictionaries with information about quizzes, that user
        created.
    """
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
    """
    individual view for AJAX request from profile page,
    returns list of dictionaries with information about quizzes, that user
    passed before (has scores in database)
    """
    quizzes = [quiz for quiz in Quiz.objects.all().order_by('-id')
               if Score.get_score(quiz.id, request.user.id) != -1]
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
    """
    Renders same page as get_all_quizzes view, but only with quizzes,
    that user haven't passed before (has no scores in database)
    """
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


@login_required
def quiz_comments(request, quiz_id, rate_id=None):
    """
    Comments page view.
    Renders comments for an individual quiz,
    user have ability to delete his comment and rate
    """
    if request.method == "DELETE":
        QuizRate.objects.get(id=rate_id).delete()
        return JsonResponse({'deleted': True})
    rates = QuizRate.objects.filter(quiz_id=quiz_id)
    quiz_name = Quiz.objects.get(id=quiz_id).name
    for rate in rates:
        rate.comment_username = CustomUser.objects.get(id=rate.user_id).username
    return render(request, 'quiz_comments.html', {'quiz_name': quiz_name,
                                                  'rates': rates,
                                                  'current_username': request.user.username})


def get_max_points(quiz_id):
    """Returns all available points fro specific quiz."""
    return Question.objects.filter(quiz_id=quiz_id).aggregate(Sum('points'))['points__sum']
