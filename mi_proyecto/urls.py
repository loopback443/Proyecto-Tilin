from django.contrib import admin
from django.urls import path, include  # 👈 esto es clave

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cuentas.urls')),  # 👈 conecta con las URLs de tu app
]
