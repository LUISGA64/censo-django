"""
Señales de seguridad para rastrear eventos de autenticación
"""
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import password_changed, password_reset
from .security_models import LoginAttempt, SecurityEvent, SessionSecurity


def get_client_ip(request):
    """Obtiene la IP del cliente desde el request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    # Si no hay IP (ej: en tests), usar IP de prueba
    if not ip:
        ip = '127.0.0.1'
    
    return ip


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Registra login exitoso"""
    # Verificar que el request tenga META (en tests puede no tenerlo)
    if not hasattr(request, 'META'):
        return
    
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    # Registrar intento exitoso
    LoginAttempt.objects.create(
        username=user.username,
        ip_address=ip_address,
        user_agent=user_agent,
        success=True
    )

    # Registrar evento de seguridad
    SecurityEvent.objects.create(
        user=user,
        event_type='login_success',
        description=f'Login exitoso desde {ip_address}',
        ip_address=ip_address,
        user_agent=user_agent
    )

    # Registrar sesión activa
    session_key = request.session.session_key
    if session_key:
        SessionSecurity.objects.update_or_create(
            session_key=session_key,
            defaults={
                'user': user,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'is_active': True
            }
        )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """Registra intento de login fallido"""
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    username = credentials.get('username', credentials.get('email', 'unknown'))

    # Registrar intento fallido
    LoginAttempt.objects.create(
        username=username,
        ip_address=ip_address,
        user_agent=user_agent,
        success=False,
        failure_reason='Credenciales inválidas'
    )

    # Verificar si debe bloquearse
    if LoginAttempt.is_blocked(username=username):
        SecurityEvent.objects.create(
            event_type='account_locked',
            description=f'Cuenta bloqueada por múltiples intentos fallidos: {username}',
            ip_address=ip_address,
            user_agent=user_agent,
            metadata={'username': username, 'attempts': 5}
        )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Registra logout de usuario"""
    if user:
        ip_address = get_client_ip(request)

        # Desactivar sesión
        session_key = request.session.session_key
        if session_key:
            SessionSecurity.objects.filter(session_key=session_key).update(is_active=False)


@receiver(password_changed)
def log_password_changed(sender, request, user, **kwargs):
    """Registra cambio de contraseña"""
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    SecurityEvent.objects.create(
        user=user,
        event_type='password_changed',
        description=f'Contraseña cambiada por el usuario',
        ip_address=ip_address,
        user_agent=user_agent
    )


@receiver(password_reset)
def log_password_reset(sender, request, user, **kwargs):
    """Registra reset de contraseña"""
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    SecurityEvent.objects.create(
        user=user,
        event_type='password_reset_complete',
        description=f'Contraseña reseteada exitosamente',
        ip_address=ip_address,
        user_agent=user_agent
    )

