from django.contrib import admin
from django.urls import path
from .views import home, user_profile, list_users, home, registration

urlpatterns = [
    path('', home, name='hello'),
    path('home/', home, name='home'),
    path('list/users', list_users, name='list_users'),
    path('accounts/registration', registration, name='registration'),
    path('<username>/', user_profile, name='user_profile'),
]
