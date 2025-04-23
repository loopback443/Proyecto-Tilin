from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ReservaForm, RegistroUsuarioForm
from .models import Reserva, CustomUser

# ========================
# VISTAS DE AUTENTICACIÓN
# ========================

def login_view(request):
    """Vista para iniciar sesión de usuario."""
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


def register_view(request):
    """Vista para registrar un nuevo usuario."""
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
    """Cierra la sesión del usuario actual y redirige al login."""
    logout(request)
    return redirect('login')


# ========================
# VISTAS DE USUARIO LOGUEADO
# ========================

@login_required
def index_view(request):
    """Vista principal del sistema para usuarios autenticados."""
    return render(request, 'cuentas/index.html', {'usuario': request.user.first_name})


@login_required
def hacer_reserva(request):
    """Procesa el formulario de reservas y guarda la reserva del usuario."""
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
    """Muestra todas las reservas hechas por el usuario logueado."""
    reservas = request.user.reserva_set.all()
    return render(request, 'cuentas/mis_reservas.html', {'reservas': reservas})


# ========================
# VISTAS ADMINISTRADOR
# ========================

def es_admin(user):
    """Valida si el usuario es administrador."""
    return user.is_authenticated and user.rol == 'admin'


@user_passes_test(es_admin)
def gestionar_usuarios(request):
    """
    Vista exclusiva para el administrador. Muestra todos los usuarios del sistema.
    Permite filtrar por nombre y rol.
    """
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
    """
    Permite al administrador editar el rol de un usuario.
    No permite modificar su propio rol.
    """
    usuario = CustomUser.objects.get(id=usuario_id)

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
    """
    Permite al administrador eliminar un usuario del sistema.
    Evita que se elimine a sí mismo.
    """
    usuario = CustomUser.objects.get(id=usuario_id)

    if request.user == usuario:
        messages.error(request, "No podés eliminar tu propio usuario.")
        return redirect('gestionar_usuarios')

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('gestionar_usuarios')

    return render(request, 'cuentas/eliminar_usuario.html', {'usuario': usuario})

@user_passes_test(es_admin)
def ver_todas_las_reservas(request):
    reservas = Reserva.objects.all()

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
    """
    Permite al admin eliminar cualquier reserva del sistema.
    """
    reserva = Reserva.objects.get(id=reserva_id)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva eliminada correctamente.")
        return redirect('ver_todas_las_reservas')

    return render(request, 'cuentas/eliminar_reserva_admin.html', {'reserva': reserva})