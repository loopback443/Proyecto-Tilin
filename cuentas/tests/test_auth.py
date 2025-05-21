from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestLogin(TestCase):
    """
    Pruebas unitarias para la autenticación de usuarios mediante el formulario de login.

    Este test valida:
    - Login con credenciales correctas.
    - Respuesta apropiada ante credenciales incorrectas.
    """

    def setUp(self):
        """
        Crea un usuario de prueba en la base de datos de testing.
        """
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_login_correct_credentials(self):
        """
        Verifica que el login funcione correctamente con credenciales válidas.
        Debe redirigir al usuario a la página de inicio.
        """
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpass123',
        })
        self.assertRedirects(response, reverse('inicio'))

    def test_login_wrong_password(self):
        """
        Verifica que el login falle al usar una contraseña incorrecta.
        Debe mostrar el mensaje de error correspondiente.
        """
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'wrongpass',
        })
        self.assertContains(response, "Correo o contraseña incorrectos.")
