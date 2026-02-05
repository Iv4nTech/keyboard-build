from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, SocialNetworkUser, SocialNetwork, Keyboard, Component, KeyboardComponent, Level, GetLevel
from .forms import RegisterUserForm, ConfigurateUserForm, CreateKeyboardForm
from django.db.models import Max
from django.views.generic import DeleteView, CreateView, ListView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
def home(request):
    return render(request, 'core/home.html')

def user_profile(request, username):
    user = User.objects.get(username=username)
    keyboards = Keyboard.objects.filter(user=user)
    return render(request,'core/user_profile.html', {'user_profile':user, 'keyboards':keyboards})

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
            messages.success(request,'Register success!')
            return redirect('home')
        for error in form.errors.as_data().values():
            for e in error: # Acceder a cada fallo
                print(f'ERROR:{e.message}') 
                messages.error(request, e.message)
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
                obj, creado =  SocialNetworkUser.objects.update_or_create(
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
            messages.success(request, 'La configuración se ha guardado correctamente')

            #Aqui poner que lleva a la misma pagina pero que le salte una messages
            return redirect('configuration_user')
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
    success_url = reverse_lazy('list_users')
    template_name = 'core/delete_user.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)

class CreateKeyboard(CreateView):
    model = Keyboard
    template_name = 'core/create_keyboard.html'
    form_class = CreateKeyboardForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        #Cogemos el nivel maximo del usuario

        user_data = GetLevel.objects.filter(user=self.object.user).aggregate(max_lvl=Max('level__number'))
        
        #Guardamos en una variable el numero y sumamos uno
        current_num = user_data['max_lvl'] or 0
        next_num = current_num + 1

        #Si no existe try
        try:
            level = Level.objects.get(number=next_num)
        except Level.DoesNotExist:
            level = Level.objects.create(
                number=next_num
            )

        # Y ahora lo creamos
        GetLevel.objects.create(
            user=self.object.user,
            level=level
        )
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username':self.request.user})
    
class ViewKeyboard(ListView):
    model = Keyboard
    template_name = 'core/view_keyboards.html'
    context_object_name = 'keyboards'

    def get_queryset(self):
        print(self.kwargs['username'])
        queryset = Keyboard.objects.filter(user__username=self.kwargs['username'])
        return queryset
    
class DetailKeyboard(DetailView):
    model = Keyboard
    context_object_name = 'keyboard'
    template_name = 'core/detail_keyboard.html'

class DeleteKeyboard(DeleteView):
    model = Keyboard
    context_object_name = 'keyboard'
    template_name = 'core/delete_keyboard.html'

    def form_valid(self, form):

        keyboard_delete = self.get_object()

        if keyboard_delete.user != self.request.user:
            return HttpResponseForbidden('You not cant eliminate keyboard by another user')

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username':self.request.user})
    
class UpdateKeyboard(UpdateView):
    model = Keyboard
    context_object_name = 'keyboard'
    template_name = 'core/update_keyboard.html'
    form_class = CreateKeyboardForm

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username':self.request.user})
    
class CreateSocialNetworkUser(TemplateView):
    template_name = 'core/add_networksocial_user.html'

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username':self.request.user})

    def post(self, request):
        social_network = request.POST.get('social-networks')
        print(social_network)
        obj_social_network = SocialNetwork.objects.get(name=social_network)
        SocialNetworkUser.objects.create(user=request.user,social_network=obj_social_network )
        return redirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['social_networks'] = SocialNetwork.objects.exclude(social_networks_user__user=self.request.user)
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        try:
            self.object.save()
        except:
            messages.error(self.request, "Esta red social ya la tienes añadida!")
            return redirect('add_socialnetwork')
        return redirect(self.get_success_url())

class DeleteNetworkSocial(DeleteView):
    model = SocialNetworkUser
    context_object_name = 'social_network'
    template_name = 'core/delete_network_social.html'
    success_url = reverse_lazy('configuration_user')

    def form_valid(self, form):

        keyboard_delete = self.get_object()

        if keyboard_delete.user != self.request.user:
            return HttpResponseForbidden('You not cant eliminate network social by another user')

        return super().form_valid(form)
    
# AHORA VIENE LO TOCHO

class ViewKeyboardComponents(ListView):
    model = KeyboardComponent
    context_object_name = 'components'
    template_name = 'core/view_keyboard_components.html'


    def get_queryset(self):
        return KeyboardComponent.objects.filter(keyboard__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyboard'] = get_object_or_404(Keyboard, id=self.kwargs['pk'])
        return context

class DetailComponent(DetailView):
    model = Component
    context_object_name = 'component'
    template_name = 'core/detail_component.html'

    def get_object(self, queryset=None):
        keyboard_id = self.kwargs.get('pk_k')
        component_id = self.kwargs.get('pk')
        return get_object_or_404(
            Component, 
            id=component_id, 
            builds__keyboard__id=keyboard_id
        )