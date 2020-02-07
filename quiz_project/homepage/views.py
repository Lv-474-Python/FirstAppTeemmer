"""homepage views"""
from django.shortcuts import render


def homepage(request):
    """
        renders homepage,
        if user is not logged in, there is only ling to login page.
    """
    user = request.user
    return render(request, 'homepage.html', {'user': user})
