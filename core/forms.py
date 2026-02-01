from django import forms
from .models import User, SocialNetworkUser, SocialNetwork
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username','email']

class ConfigurateUserForm(forms.Form):
    image = forms.ImageField()
    bio = forms.CharField()
    social_networks = forms.ModelChoiceField(
        queryset=SocialNetwork.objects.none(), empty_label='Selecciona una red social...'
    )
    username_network = forms.CharField(max_length=15)
    url = forms.URLField()

    def __init__(self, *args, **kwargs): # Con esto conseguimos que al instanciar el objeto pues la queryset del choices cambia con las redes sociales que tiene el usuario
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        if user:
            self.fields['social_networks'].queryset = SocialNetwork.objects.filter(social_networks_user__user=user)