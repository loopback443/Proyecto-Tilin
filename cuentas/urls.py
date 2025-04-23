from django.urls import path
from .views import (
    login_view,
    logout_view,
    register_view,
    index_view,
    hacer_reserva,
    mis_reservas,
    gestionar_usuarios,
    editar_usuario,
    eliminar_usuario,
    ver_todas_las_reservas,
    eliminar_reserva_admin
)

urlpatterns = [
    # Páginas generales del usuario
    path('', index_view, name='inicio'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('reservar/', hacer_reserva, name='hacer_reserva'),
    path('mis-reservas/', mis_reservas, name='mis_reservas'),

    # Gestión de usuarios (solo para admin)
    path('usuarios/', gestionar_usuarios, name='gestionar_usuarios'),
    path('usuarios/editar/<int:usuario_id>/', editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),

    # Gestión de reservas del sistema (solo para admin)
    path('reservas-todas/', ver_todas_las_reservas, name='ver_todas_las_reservas'),
    path('reservas/eliminar/<int:reserva_id>/', eliminar_reserva_admin, name='eliminar_reserva_admin'),
]
