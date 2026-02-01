from django import forms
from .models import User, SocialNetworkUser, SocialNetwork
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username','email']

class ConfigurateUserForm(forms.Form):
    image = forms.ImageField(required=False)
    bio = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    dateofbirth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=False)
    social_networks = forms.ModelChoiceField(
        queryset=SocialNetwork.objects.none(), empty_label='Select social network...', required=False
    )
    username_network = forms.CharField(max_length=15, required=False)
    url = forms.URLField(required=False)

    def __init__(self, *args, **kwargs): # Con esto conseguimos que al instanciar el objeto pues la queryset del choices cambia con las redes sociales que tiene el usuario
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        if user:
            self.fields['social_networks'].queryset = SocialNetwork.objects.filter(social_networks_user__user=user)