from django.shortcuts import render, redirect


def get_profile(request):
    user = request.user
    if user.is_anonymous:
        return redirect('login')
    return render(request, 'profile.html', {'user': user})

