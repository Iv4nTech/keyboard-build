from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from .forms import RegisterUserForm

def home(request):
    return render(request, 'core/home.html')

def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request,'core/user_profile.html', {'user_profile':user})

def list_users(request):
    users = User.objects.all()
    return render(request, 'core/list_users.html', {'users':users})

def registration(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            print('Formulario guardado!')
            return redirect('list_users')
    form = RegisterUserForm()
    return render(request, 'registration/registration.html', {'form':form})
            