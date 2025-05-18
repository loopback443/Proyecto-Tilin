from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ReservaForm, RegistroUsuarioForm, ComidaForm
from .models import Reserva, CustomUser, Comida

# ========================
# FUNCIONES AUXILIARES
# ========================

def es_admin(user):
    return user.is_authenticated and user.rol == 'admin'

def es_admin_o_recepcionista(user):
    return user.is_authenticated and user.rol in ['admin', 'recepcionista']

# ========================
# AUTENTICACIÓN
# ========================

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.rol == 'admin':
                return redirect('inicio')
            elif user.rol == 'recepcionista':
                return redirect('ver_todas_las_reservas')
            else:
                return redirect('inicio')
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
    return render(request, 'cuentas/login.html')


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


def logout_view(request):
    logout(request)
    return redirect('login')

# ========================
# CLIENTE: INICIO / RESERVAS
# ========================

@login_required
def index_view(request):
    return render(request, 'cuentas/index.html', {'usuario': request.user.first_name})


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
    reservas = request.user.reserva_set.filter(activa=True)
    return render(request, 'cuentas/mis_reservas.html', {'reservas': reservas})


@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user, activa=True)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva actualizada con éxito.")
            return redirect('mis_reservas')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'cuentas/form_reserva.html', {'form': form, 'accion': 'Editar'})


@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente=request.user, activa=True)

    if request.method == 'POST':
        reserva.activa = False
        reserva.save()
        messages.success(request, "Reserva cancelada correctamente.")
        return redirect('mis_reservas')

    return render(request, 'cuentas/confirmar_cancelacion.html', {'reserva': reserva})

# ========================
# ADMIN: GESTIÓN DE USUARIOS
# ========================

@user_passes_test(es_admin)
def gestionar_usuarios(request):
    usuarios = CustomUser.objects.all()
    filtro_nombre = request.GET.get('nombre', '')
    filtro_rol = request.GET.get('rol', '')

    if filtro_nombre:
        usuarios = usuarios.filter(first_name__icontains=filtro_nombre)
    if filtro_rol:
        usuarios = usuarios.filter(rol__iexact=filtro_rol)

    return render(request, 'cuentas/gestionar_usuarios.html', {
        'usuarios': usuarios,
        'filtro_nombre': filtro_nombre,
        'filtro_rol': filtro_rol,
    })


@user_passes_test(es_admin)
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)

    if request.user == usuario:
        messages.error(request, "No podés modificar tu propio rol.")
        return redirect('gestionar_usuarios')

    if request.method == 'POST':
        nuevo_rol = request.POST.get('rol')
        if nuevo_rol in ['admin', 'recepcionista', 'cliente']:
            usuario.rol = nuevo_rol
            usuario.save()
            messages.success(request, "Rol actualizado correctamente.")
        else:
            messages.error(request, "Rol inválido.")
        return redirect('gestionar_usuarios')

    return render(request, 'cuentas/editar_usuario.html', {'usuario': usuario})


@user_passes_test(es_admin)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)

    if request.user == usuario:
        messages.error(request, "No podés eliminar tu propio usuario.")
        return redirect('gestionar_usuarios')

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('gestionar_usuarios')

    return render(request, 'cuentas/eliminar_usuario.html', {'usuario': usuario})

# ========================
# RESERVAS (ADMIN/RECEPCIONISTA)
# ========================

@user_passes_test(es_admin_o_recepcionista)
def ver_todas_las_reservas(request):
    reservas = Reserva.objects.all()  # Incluye activas e inactivas
    nombre = request.GET.get('nombre', '')
    contacto = request.GET.get('contacto', '')
    fecha = request.GET.get('fecha', '')

    if nombre:
        reservas = reservas.filter(cliente__first_name__icontains=nombre)
    if contacto:
        reservas = reservas.filter(nombre_contacto__icontains=contacto)
    if fecha:
        reservas = reservas.filter(fecha=fecha)

    return render(request, 'cuentas/ver_todas_las_reservas.html', {
        'reservas': reservas,
        'filtro_nombre': nombre,
        'filtro_contacto': contacto,
        'filtro_fecha': fecha,
    })


@user_passes_test(es_admin)
def eliminar_reserva_admin(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva eliminada correctamente.")
        return redirect('ver_todas_las_reservas')
    return render(request, 'cuentas/eliminar_reserva_admin.html', {'reserva': reserva})

# ========================
# MENÚ Y COMIDAS
# ========================

@login_required
def menu_view(request):
    menu = Comida.objects.all()
    return render(request, 'cuentas/menu.html', {'menu': menu})


@user_passes_test(es_admin)
def gestionar_comidas(request):
    comidas = Comida.objects.all()
    return render(request, 'cuentas/gestionar_comidas.html', {'comidas': comidas})


@user_passes_test(es_admin)
def agregar_comida(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comida agregada correctamente.')
            return redirect('gestionar_comidas')
    else:
        form = ComidaForm()
    return render(request, 'cuentas/form_comida.html', {'form': form, 'accion': 'Agregar'})


@user_passes_test(es_admin)
def editar_comida(request, comida_id):
    comida = get_object_or_404(Comida, id=comida_id)
    if request.method == 'POST':
        form = ComidaForm(request.POST, instance=comida)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comida actualizada correctamente.')
            return redirect('gestionar_comidas')
    else:
        form = ComidaForm(instance=comida)
    return render(request, 'cuentas/form_comida.html', {'form': form, 'accion': 'Editar'})


@user_passes_test(es_admin)
def eliminar_comida(request, comida_id):
    comida = get_object_or_404(Comida, id=comida_id)
    comida.delete()
    messages.success(request, 'Comida eliminada correctamente.')
    return redirect('gestionar_comidas')
