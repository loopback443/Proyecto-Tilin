from django.urls import path
from .views import (
    login_view,
    logout_view,
    register_view,
    index_view
)

urlpatterns = [
    path('', index_view, name='inicio'),            # Página principal (requiere login)
    path('login/', login_view, name='login'),       # Formulario de login
    path('logout/', logout_view, name='logout'),    # Cerrar sesión
    path('register/', register_view, name='register')  # Registro de nuevos usuarios
]
