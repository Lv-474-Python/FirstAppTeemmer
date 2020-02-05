from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

from users.models import CustomUser


def get_profile(request):
    user = request.user
    if user.is_anonymous:
        return redirect('login')
    return render(request, 'profile.html', {'user': user})


@login_required(login_url='/users/login/')
def change_password(request):
    if request.method == "GET":
        return render(request, 'change_password.html')
    cur_pass = request.user.password
    old_pass = request.POST.get('old_password')
    new_pass = request.POST.get('new_password')
    if check_password(old_pass, cur_pass):
        user = CustomUser.change_password(username=request.user.username,
                                          new_password=new_pass)
        update_session_auth_hash(request, user)
        return redirect('get_profile')
    return render(request, 'change_password.html', {'error': 'Wrong old password'})
