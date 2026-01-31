from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from .forms import RegisterUserForm
from django.db.models import Max
def home(request):
    return render(request, 'core/home.html')

def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request,'core/user_profile.html', {'user_profile':user})

def list_users(request):
    users = User.objects.all()
    username = request.GET.get('username')
    level = request.GET.get('level')
    if username:
        users = users.filter(username__icontains = username)
    if level:
        users = users.filter(level__gt=level)
    return render(request, 'core/list_users.html', {'users':users})

def ranking_users(request):
    users = User.objects.annotate(max_level=Max('levels__level__number')).order_by('-max_level')
    return render(request, 'core/ranking_users.html',  {'users':users})

def registration(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            print('Formulario guardado!')
            return redirect('list_users')
    form = RegisterUserForm()
    return render(request, 'registration/registration.html', {'form':form})
            