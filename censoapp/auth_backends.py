"""
Backend de autenticación personalizado con protección contra fuerza bruta
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from .security_models import LoginAttempt


User = get_user_model()


class SecureAuthBackend(ModelBackend):
    """
    Backend de autenticación que valida si el usuario/IP está bloqueado
    antes de permitir el login
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica al usuario verificando primero si está bloqueado
        """
        if username is None or password is None:
            return None

        # Obtener IP del usuario
        ip_address = self._get_client_ip(request)

        # Verificar si el usuario o IP está bloqueado
        if LoginAttempt.is_blocked(username=username, max_attempts=5, timeout_minutes=5):
            raise PermissionDenied(
                "Su cuenta ha sido temporalmente bloqueada por múltiples intentos de inicio de sesión fallidos. "
                "Por favor intente nuevamente en 5 minutos."
            )

        if LoginAttempt.is_blocked(ip_address=ip_address, max_attempts=10, timeout_minutes=5):
            raise PermissionDenied(
                "Esta dirección IP ha sido temporalmente bloqueada por múltiples intentos de inicio de sesión fallidos. "
                "Por favor intente nuevamente en 5 minutos."
            )

        # Proceder con la autenticación normal
        return super().authenticate(request, username=username, password=password, **kwargs)

    def _get_client_ip(self, request):
        """Obtiene la IP del cliente desde el request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

