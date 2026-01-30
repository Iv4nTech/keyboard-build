from django.contrib import admin
from django.urls import path
from .views import home, user_profile

urlpatterns = [
    path('', home, name='hello'),
    path('<username>/', user_profile, name='user_profile'),
]
