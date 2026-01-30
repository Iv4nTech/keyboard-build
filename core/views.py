from django.shortcuts import render
from django.http import HttpResponse
from .models import User

def home(request):
    return HttpResponse('Home')

def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request,'core/user_profile.html', {'user_profile':user})