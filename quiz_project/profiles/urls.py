from django.urls import path, include

from .views import get_profile, change_password

urlpatterns = [
    path('profile/', get_profile, name='get_profile'),
    path('change_pass/', change_password, name='change_password'),
]
