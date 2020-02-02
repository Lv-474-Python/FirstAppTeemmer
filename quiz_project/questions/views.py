from django.shortcuts import render, redirect

from answers.models import Answer
from questions.models import Question
from answers.views import get_answers

