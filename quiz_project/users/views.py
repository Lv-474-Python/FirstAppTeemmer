from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.backends import django

from users.models import CustomUser


def get_all_users(request):
    return render(request, 'users.html', {'all_users': CustomUser.objects.all()})


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    if request.POST.get('check_username'):
        if CustomUser.objects.filter(username=str(request.POST['check_username'])):
            return JsonResponse({'name_available': False})
        return JsonResponse({'name_available': True})
    if request.POST.get('check_mail'):
        if CustomUser.objects.filter(email=str(request.POST['check_mail'])):
            return JsonResponse({'mail_available': False})
        return JsonResponse({'mail_available': True})
    name = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    user = CustomUser.create(username=name, password=password, email=email)
    if user:
        user.is_active = True
        user.save()
        return redirect('login')
    return render(request, 'register.html')


def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    name = request.POST['username']
    password = request.POST['password']
    if CustomUser.objects.filter(username=name):
        user = authenticate(username=name, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('homepage')
        return render(request, 'login.html', {'error': 'Wrong password', 'username': name})
    return render(request, 'login.html', {'error': 'No such user'})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')




