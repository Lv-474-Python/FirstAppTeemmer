from django.urls import path, include

from .views import get_all_users, login_user, register

urlpatterns = [
    path('', include('profiles.urls')),
    path('', get_all_users, name='get_all_users'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),

]
