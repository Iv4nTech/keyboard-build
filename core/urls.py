from django.contrib import admin
from django.urls import path
from .views import home, user_profile, list_users, home, registration,ranking_users, configuration_user, UserDeleteView

urlpatterns = [
    path('', home, name='hello'),
    path('home/', home, name='home'),
    path('list/users/', list_users, name='list_users'),
    path('accounts/registration/', registration, name='registration'),
    path('users/ranking/', ranking_users, name='ranking_users'),
    path('user/configuration/', configuration_user, name='configuration_user'),
    path('user/configuration/delete_user/<username>', UserDeleteView.as_view(), name='delete_user'),
    path('profile/<username>/', user_profile, name='user_profile'),
]
