from django.contrib import admin
from .models import Mesa, Reserva
from .models import Comida

admin.site.register(Mesa)
admin.site.register(Reserva)

@admin.register(Comida)
class ComidaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio']
    search_fields = ['nombre']