from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.backends import django

from users.models import CustomUser


def get_all_users(request):
    return render(request, 'users.html', {'all_users': CustomUser.objects.all()})


def register(request):
    name = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    user = CustomUser.create(username=name, password=password, email=email)
    if user:
        return redirect('login')
    return HttpResponse('bida', status=400)


def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'all_users': CustomUser.objects.all()})
    name = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=name, password=password)
    if user and user.is_active:
        login(request, user)
        return redirect('homepage')
    return redirect('login')



