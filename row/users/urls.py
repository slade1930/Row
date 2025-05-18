from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # Las URLs de login/logout las maneja django.contrib.auth.urls
]