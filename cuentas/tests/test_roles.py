from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestRoles(TestCase):
    """
    Pruebas unitarias para verificar el comportamiento de los diferentes roles de usuario en el sistema:
    - Administrador
    - Recepcionista
    - Cliente
    """

    def setUp(self):
        """
        Crea usuarios de prueba para cada tipo de rol:
        admin, recepcionista y cliente.
        """
        User = get_user_model()
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            rol='admin'
        )
        self.recepcionista = User.objects.create_user(
            email='recep@example.com',
            password='recep123',
            first_name='Recep',
            last_name='User',
            rol='recepcionista'
        )
        self.cliente = User.objects.create_user(
            email='cliente@example.com',
            password='cliente123',
            first_name='Cliente',
            last_name='User',
            rol='cliente'
        )

    def test_recepcionista_redirige_a_reservas(self):
        """
        Verifica que un recepcionista sea redirigido automáticamente
        a la vista de todas las reservas al intentar acceder a 'inicio'.
        """
        self.client.login(email='recep@example.com', password='recep123')
        response = self.client.get(reverse('inicio'))
        self.assertRedirects(response, reverse('ver_todas_las_reservas'))

    def test_cliente_no_accede_a_usuarios(self):
        """
        Verifica que un cliente no tenga acceso a la vista de gestión de usuarios.
        """
        self.client.login(email='cliente@example.com', password='cliente123')
        response = self.client.get(reverse('gestionar_usuarios'))
        self.assertEqual(response.status_code, 403)  # Acceso prohibido

    def test_admin_tiene_acceso_total(self):
        """
        Verifica que un administrador tenga acceso a la gestión de usuarios.
        """
        self.client.login(email='admin@example.com', password='admin123')
        response = self.client.get(reverse('gestionar_usuarios'))
        self.assertEqual(response.status_code, 200)
