from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from .models import User, Profile

# Formulario para el registro de usuarios
class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Repetir contraseña")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password1']

    # Validar si ya existe un usuario igual
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ya existe ese usuario, intenta otro usuario.")

    # Validar las contraseñas
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if password and password1 and password != password1:
            raise("Las contraseñas no coinciden.")

# Formulario para mostrar/actualizar el perfil
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']


    