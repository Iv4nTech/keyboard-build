from django.shortcuts import render
from django.http import HttpResponse
from .models import User

def home(request):
    return render(request, 'core/home.html')

def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request,'core/user_profile.html', {'user_profile':user})

def list_users(request):
    users = User.objects.all()
    return render(request, 'core/list_users.html', {'users':users})