from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Importamos tu modelo personalizado
from .models import Reserva

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        exclude = ['cliente']  # El cliente se asigna automáticamente desde request.user