from django.contrib import admin
from django.urls import path
from .views import home, user_profile, list_users, home, registration,ranking_users, configuration_user, UserDeleteView, CreateKeyboard, ViewKeyboard, DetailKeyboard, DeleteKeyboard, UpdateKeyboard, CreateSocialNetworkUser, DeleteNetworkSocial, ViewKeyboardComponents, DetailComponent
urlpatterns = [
    path('', home, name='hello'),
    path('home/', home, name='home'),
    path('list/users/', list_users, name='list_users'),
    path('accounts/registration/', registration, name='registration'),
    path('users/ranking/', ranking_users, name='ranking_users'),
    path('user/configuration/', configuration_user, name='configuration_user'),
    path('user/configuration/delete_user/<username>', UserDeleteView.as_view(), name='delete_user'),
    path('profile/<username>/', user_profile, name='user_profile'),
    path('profile/create/keyboard', CreateKeyboard.as_view(), name='create_keyboard'),
    path('profile/view/keyboards', ViewKeyboard.as_view(), name='view_keyboard'),
    path('detail/keyboard/<int:pk>', DetailKeyboard.as_view(), name='detail_keyboard'),
    path('delete/keyboard/<int:pk>', DeleteKeyboard.as_view(), name='delete_keyboard'),
    path('update/keyboard/<int:pk>', UpdateKeyboard.as_view(), name='update_keyboard'),
    path('profile/networksocial/add_socialnetwork', CreateSocialNetworkUser.as_view(), name='add_socialnetwork'),
    path('profile/networksocial/delete_socialnetwork/<int:pk>', DeleteNetworkSocial.as_view(), name='delete_socialnetwork'),
    path('detail/keyboard/<int:pk>/view/components', ViewKeyboardComponents.as_view(), name='view_components'),
    path('detail/keyboard/<int:pk_k>/detail/component/<int:pk>', DetailComponent.as_view() , name='detail_components')

]
