from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestGestionUsuarios(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user(
            email='admin@example.com',
            password='adminpass',
            first_name='Admin',
            last_name='User',
            rol='admin',
            is_superuser=True,
            is_staff=True
        )
        self.client.login(email='admin@example.com', password='adminpass')

    def test_acceso_gestion_usuarios(self):
        response = self.client.get(reverse('gestionar_usuarios'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gestión de Usuarios")

    def test_editar_usuario(self):
        user = get_user_model().objects.create_user(
            email='cliente@example.com',
            password='clientepass',
            first_name='Cliente',
            last_name='Ejemplo',
            rol='cliente'
        )
        response = self.client.post(reverse('editar_usuario', args=[user.id]), {
            'rol': 'recepcionista'
        })
        user.refresh_from_db()
        self.assertEqual(user.rol, 'recepcionista')
