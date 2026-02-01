from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, SocialNetworkUser, SocialNetwork
from .forms import RegisterUserForm, ConfigurateUserForm
from django.db.models import Max
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import logout
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
        users = User.objects.annotate(max_level=Max('levels__level__number')).order_by('-max_level')
        users = users.filter(max_level__gt=level)
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

def configuration_user(request):
    user = request.user

    if request.method == 'POST':
        form = ConfigurateUserForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            bio = form.cleaned_data['bio']
            image = form.cleaned_data['image']
            social_network = form.cleaned_data['social_networks']
            username_network = form.cleaned_data['username_network']
            url = form.cleaned_data['url']
            dateofbirth = form.cleaned_data['dateofbirth']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if social_network:
                SocialNetworkUser.objects.update_or_create(
                    user=user,
                    social_network = social_network,
                    defaults={'username':username_network, 'url':url},
                )

            user.bio = bio
            user.image = image
            user.first_name = first_name
            user.last_name = last_name
            user.dateofbirth = dateofbirth
            user.save()

            #Aqui poner que lleva a la misma pagina pero que le salte una messages
            return redirect('list_users')
        else:
            print(form.errors.as_data())
    data_initial = {'bio':user.bio,
                    'image':user.image,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'dateofbirth':user.dateofbirth}


    networks_socials = SocialNetworkUser.objects.filter(user=user).select_related('social_network')

    form = ConfigurateUserForm(initial=data_initial, user=user)
    return render(request, 'core/configuration_user.html', {'form':form, 'network_social':networks_socials})

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('lists_user')
    template_name = 'core/delete_user.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def form_valid(self, form):
        user = self.get_object()
        logout(self.request)
        user.delete()
        return redirect('home')
