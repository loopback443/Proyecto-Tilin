from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Importamos tu modelo personalizado

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
