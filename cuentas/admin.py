from django.contrib import admin
from .models import Mesa, Reserva, Comida

# ============================
# REGISTRO DE MODELOS EN ADMIN
# ============================

# Registra el modelo Mesa en el panel de administración de Django.
admin.site.register(Mesa)

# Registra el modelo Reserva para que los administradores puedan gestionarlo.
admin.site.register(Reserva)

# Configura cómo se mostrará el modelo Comida en el admin.
@admin.register(Comida)
class ComidaAdmin(admin.ModelAdmin):
    """
    Clase personalizada para administrar objetos del modelo Comida en el panel admin.

    Atributos:
        list_display: columnas que se mostrarán en la lista (nombre y precio).
        search_fields: campos habilitados para búsqueda.
    """
    list_display = ['nombre', 'precio']
    search_fields = ['nombre']
