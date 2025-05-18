from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Reserva, Comida

class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario personalizado para registrar nuevos usuarios.

    Basado en UserCreationForm de Django, utiliza el modelo CustomUser
    con email como identificador principal. Incluye los campos:
    - Nombre
    - Apellido
    - Correo electrónico
    - Contraseña (2 veces para confirmación)
    """
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class ReservaForm(forms.ModelForm):
    """
    Formulario para realizar reservas.

    Está basado en el modelo Reserva, y excluye el campo 'cliente',
    ya que se asigna automáticamente con request.user en la vista.
    """
    class Meta:
        model = Reserva
        exclude = ['cliente']


class ComidaForm(forms.ModelForm):
    """
    Formulario para agregar o editar comidas del menú.

    Basado en el modelo Comida, incluye los campos:
    - nombre
    - precio
    """
    class Meta:
        model = Comida
        fields = ['nombre', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }
