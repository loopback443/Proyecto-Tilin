from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm
from .models import Reserva

from .forms import RegistroUsuarioForm

# LOGIN
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
    return render(request, 'cuentas/login.html')

# REGISTRO
def register_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = RegistroUsuarioForm()
    return render(request, 'cuentas/register.html', {'form': form})

# INDEX (requiere login)
@login_required
def index_view(request):
    return render(request, 'cuentas/index.html', {'usuario': request.user.first_name})

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@login_required
def hacer_reserva(request):
    if request.method == 'POST':
        reserva = Reserva(
            cliente=request.user,
            fecha=request.POST.get('fecha'),
            hora=request.POST.get('hora'),
            cantidad_personas=request.POST.get('cantidad_personas'),
            motivo=request.POST.get('motivo'),
            nombre_contacto=request.POST.get('nombre_contacto'),
            correo=request.POST.get('correo'),
            telefono=request.POST.get('telefono'),
            notas_adicionales=request.POST.get('notas_adicionales')
        )
        reserva.save()
        messages.success(request, "¡Reserva realizada con éxito!")
        return redirect('inicio')
    return redirect('inicio')
    


@login_required
def mis_reservas(request):
    reservas = request.user.reserva_set.all()
    return render(request, 'cuentas/mis_reservas.html', {'reservas': reservas})