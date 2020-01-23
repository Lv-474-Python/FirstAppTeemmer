from django.urls import path, include

from .views import get_profile

urlpatterns = [
    path('profile/', get_profile, name='get_profile'),
]
