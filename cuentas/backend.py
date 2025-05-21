from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailBackend(ModelBackend):
    """
    Backend de autenticación personalizado que permite iniciar sesión usando el correo electrónico en lugar del nombre de usuario.

    Hereda de:
        ModelBackend (de Django)

    Métodos:
        authenticate(request, email, password, **kwargs): autentica un usuario por correo electrónico y contraseña.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Intenta autenticar un usuario usando el campo `email` como identificador en lugar de `username`.

        Args:
            request: objeto HttpRequest (puede ser None).
            email (str): correo electrónico ingresado por el usuario.
            password (str): contraseña ingresada por el usuario.

        Returns:
            CustomUser si las credenciales son correctas, None en caso contrario.
        """
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
