from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def get_profile(request):
    user = request.user
    if user.is_anonymous:
        return redirect('login')
    return render(request, 'profile.html', {'user': user})


@login_required(login_url='/users/login/')
def change_password(request):
    if request.method == "GET":
        return render(request, 'change_password.html')
    new_pass = request.POST.get('new_password')
    request.user.set_password(new_pass)
    return redirect('profile')

