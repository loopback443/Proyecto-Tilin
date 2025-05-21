from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cuentas.models import Reserva, Mesa

class TestReservas(TestCase):
    """
    Pruebas unitarias para el módulo de reservas del sistema.

    Casos cubiertos:
    - Un cliente puede crear una reserva.
    - Cancelar una reserva marca el campo `activa` como False.
    """

    def setUp(self):
        """
        Crea un cliente de prueba y una mesa disponible para usar en las reservas.
        """
        self.user = get_user_model().objects.create_user(
            email='cliente@example.com',
            password='test123',
            first_name='Cliente',
            last_name='Uno'
        )
        self.mesa = Mesa.objects.create(numero=1, capacidad=4)
        self.client.login(email='cliente@example.com', password='test123')

    def test_cliente_puede_crear_reserva(self):
        """
        Verifica que un cliente pueda enviar un formulario válido de reserva y se cree correctamente.
        """
        response = self.client.post(reverse('hacer_reserva'), {
            'fecha': '2025-05-25',
            'hora': '20:00',
            'cantidad_personas': 2,
            'motivo': 'cena',
            'nombre_contacto': 'Cliente Uno',
            'correo': 'cliente@example.com',
            'telefono': '098112233',
            'notas_adicionales': '',
            'mesa': self.mesa.id
        })
        self.assertEqual(response.status_code, 302)  # Redirección tras éxito
        self.assertEqual(Reserva.objects.count(), 1)

    def test_cancelar_reserva_pone_activa_en_false(self):
        """
        Verifica que al cancelar una reserva, el campo `activa` se establezca en False.
        """
        reserva = Reserva.objects.create(
            cliente=self.user,
            mesa=self.mesa,
            fecha='2025-05-25',
            hora='20:00',
            cantidad_personas=2,
            motivo='cena',
            nombre_contacto='Cliente Uno',
            correo='cliente@example.com',
            telefono='098112233',
            notas_adicionales='',
            activa=True
        )
        response = self.client.post(reverse('cancelar_reserva', args=[reserva.id]))
        reserva.refresh_from_db()
        self.assertFalse(reserva.activa)
