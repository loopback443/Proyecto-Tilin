from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cuentas.models import Comida

class TestMenu(TestCase):
    """
    Pruebas unitarias para verificar la funcionalidad del módulo de menú y comidas.

    Se validan tres casos:
    - Que un administrador pueda agregar una comida.
    - Que un cliente pueda visualizar el menú.
    - Que un recepcionista no tenga acceso a la creación de comidas.
    """

    def setUp(self):
        """
        Crea usuarios de prueba: un administrador y un cliente.
        """
        User = get_user_model()
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            rol='admin'
        )
        self.cliente = User.objects.create_user(
            email='cliente@example.com',
            password='cliente123',
            first_name='Cliente',
            last_name='Uno',
            rol='cliente'
        )

    def test_admin_puede_agregar_comida(self):
        """
        Verifica que un administrador pueda agregar una comida correctamente.
        """
        self.client.login(email='admin@example.com', password='admin123')
        response = self.client.post(reverse('agregar_comida'), {
            'nombre': 'Sopa Paraguaya',
            'precio': 25000
        })
        self.assertEqual(response.status_code, 302)  # Redirección tras éxito
        self.assertTrue(Comida.objects.filter(nombre='Sopa Paraguaya').exists())

    def test_cliente_ve_menu(self):
        """
        Verifica que un cliente autenticado pueda acceder a la vista del menú.
        """
        self.client.login(email='cliente@example.com', password='cliente123')
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Menú")

    def test_recepcionista_no_puede_agregar_comida(self):
        """
        Verifica que un recepcionista no tenga permiso para acceder a la vista de agregar comida.
        """
        recepcionista = get_user_model().objects.create_user(
            email='recep@example.com',
            password='recep123',
            first_name='Recep',
            last_name='User',
            rol='recepcionista'
        )
        self.client.login(email='recep@example.com', password='recep123')
        response = self.client.get(reverse('agregar_comida'))
        self.assertEqual(response.status_code, 403)  # Acceso denegado
