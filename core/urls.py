from django.contrib import admin
from django.urls import path
from .views import home, user_profile, list_users

urlpatterns = [
    path('', home, name='hello'),
    path('<username>/', user_profile, name='user_profile'),
    path('users/', list_users, name='list_users')
]
