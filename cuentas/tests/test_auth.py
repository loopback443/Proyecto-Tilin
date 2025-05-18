from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestLogin(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_login_correct_credentials(self):
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpass123',
        })
        self.assertRedirects(response, reverse('inicio'))

    def test_login_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'wrongpass',
        })
        self.assertContains(response, "Correo o contraseña incorrectos.")
