"""
Rutas principales del sitio.

Incluye:
- Rutas de autenticación (login, logout, registro).
- Rutas para usuarios autenticados (hacer, editar, cancelar reservas).
- Rutas exclusivas para administradores (gestión de usuarios, reservas, comidas).
"""

from django.urls import path
from .views import (
    login_view,
    logout_view,
    register_view,
    index_view,
    hacer_reserva,
    mis_reservas,
    editar_reserva,
    cancelar_reserva,
    gestionar_usuarios,
    editar_usuario,
    eliminar_usuario,
    ver_todas_las_reservas,
    eliminar_reserva_admin,
    menu_view,
    agregar_comida,
    editar_comida,
    gestionar_comidas,
    eliminar_comida,
)

urlpatterns = [
    # Página de inicio
    path('', index_view, name='inicio'),

    # Autenticación
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    # Funcionalidades del cliente
    path('reservar/', hacer_reserva, name='hacer_reserva'),
    path('mis-reservas/', mis_reservas, name='mis_reservas'),
    path('reservas/editar/<int:reserva_id>/', editar_reserva, name='editar_reserva'),
    path('reservas/cancelar/<int:reserva_id>/', cancelar_reserva, name='cancelar_reserva'),

    # Administración de usuarios
    path('usuarios/', gestionar_usuarios, name='gestionar_usuarios'),
    path('usuarios/editar/<int:usuario_id>/', editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),

    # Administración de reservas (admin / recepcionista)
    path('reservas-todas/', ver_todas_las_reservas, name='ver_todas_las_reservas'),
    path('reservas/eliminar/<int:reserva_id>/', eliminar_reserva_admin, name='eliminar_reserva_admin'),

    # Menú y gestión de comidas
    path('menu/', menu_view, name='menu'),
    path('menu/gestionar/', gestionar_comidas, name='gestionar_comidas'),
    path('menu/agregar/', agregar_comida, name='agregar_comida'),
    path('menu/editar/<int:comida_id>/', editar_comida, name='editar_comida'),
    path('menu/eliminar/<int:comida_id>/', eliminar_comida, name='eliminar_comida'),
]
