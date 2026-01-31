from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username','email']