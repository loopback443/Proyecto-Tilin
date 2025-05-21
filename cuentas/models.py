from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ==============================
# MODELO CUSTOMUSER
# ==============================

class CustomUserManager(BaseUserManager):
    """
    Manager personalizado para el modelo CustomUser.
    Permite crear usuarios y superusuarios con email como identificador principal.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Crea un usuario normal con email y contraseña.
        """
        if not email:
            raise ValueError("El correo electrónico es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea un superusuario con permisos de administrador.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'admin')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado basado en email.

    Atributos:
    - email: Correo electrónico único para autenticación.
    - first_name: Nombre del usuario.
    - last_name: Apellido del usuario.
    - rol: Rol del usuario (cliente, recepcionista o administrador).
    - is_active: Estado de activación del usuario.
    - is_staff: Acceso al panel de administración.
    """

    ROL_CHOICES = [
        ('cliente', 'Cliente'),
        ('recepcionista', 'Recepcionista'),
        ('admin', 'Administrador'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# ==============================
# MODELO MESA
# ==============================

class Mesa(models.Model):
    """
    Representa una mesa disponible en el restaurante.

    Atributos:
    - numero: Número identificador único de la mesa.
    - capacidad: Número máximo de personas que admite la mesa.
    - disponible: Indica si la mesa está libre o no.
    """
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Mesa {self.numero} - {'Disponible' if self.disponible else 'Ocupada'}"


# ==============================
# MODELO RESERVA
# ==============================

class Reserva(models.Model):
    """
    Registro de una reserva hecha por un cliente.

    Atributos:
    - cliente: Usuario que realiza la reserva.
    - mesa: Mesa asignada (puede ser nula).
    - fecha: Fecha de la reserva.
    - hora: Hora de la reserva.
    - cantidad_personas: Número de personas que asistirán.
    - motivo: Motivo del evento (cumpleaños, cena, etc.).
    - nombre_contacto: Nombre del responsable de la reserva.
    - correo: Correo de contacto.
    - telefono: Teléfono del contacto.
    - notas_adicionales: Comentarios o peticiones extras.
    - activa: Indica si la reserva sigue activa o fue cancelada.
    """

    OPCIONES_MOTIVO = [
        ('cena', 'Cena normal'),
        ('birthday', 'Cumpleaños'),
        ('anniversary', 'Aniversario'),
        ('business', 'Reunión de negocios'),
        ('babyshower', 'Baby Shower'),
        ('other', 'Otro evento especial'),
    ]

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    cantidad_personas = models.PositiveIntegerField()
    motivo = models.CharField(max_length=20, choices=OPCIONES_MOTIVO, default='cena')
    nombre_contacto = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    notas_adicionales = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        estado = "Activa" if self.activa else "Cancelada"
        return f"Reserva de {self.cliente.email} el {self.fecha} a las {self.hora} ({estado})"


# ==============================
# MODELO COMIDA
# ==============================

class Comida(models.Model):
    """
    Representa un plato o ítem del menú del restaurante.

    Atributos:
    - nombre: Nombre del plato.
    - precio: Precio en guaraníes.
    """
    nombre = models.CharField(max_length=100)
    precio = models.PositiveIntegerField(help_text="Precio en guaraníes")

    def __str__(self):
        return f"{self.nombre} - Gs. {self.precio}"
