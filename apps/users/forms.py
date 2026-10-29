from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

# Formulario para el registro de usuarios
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

# Formulario para mostrar/actualizar el perfil
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']


    