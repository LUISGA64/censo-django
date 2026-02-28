"""
Modelos de seguridad para el sistema de autenticación
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class LoginAttempt(models.Model):
    """
    Rastrea intentos de inicio de sesión fallidos
    """
    username = models.CharField(max_length=150, db_index=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    failure_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Intento de Login'
        verbose_name_plural = 'Intentos de Login'
        indexes = [
            models.Index(fields=['username', '-timestamp']),
            models.Index(fields=['ip_address', '-timestamp']),
        ]

    def __str__(self):
        status = "Exitoso" if self.success else "Fallido"
        return f"{self.username} - {status} - {self.timestamp}"

    @classmethod
    def is_blocked(cls, username=None, ip_address=None, max_attempts=5, timeout_minutes=5):
        """
        Verifica si un usuario o IP está bloqueado por intentos fallidos
        """
        time_threshold = timezone.now() - timedelta(minutes=timeout_minutes)

        query = cls.objects.filter(
            success=False,
            timestamp__gte=time_threshold
        )

        if username:
            query = query.filter(username=username)
        elif ip_address:
            query = query.filter(ip_address=ip_address)
        else:
            return False

        failed_attempts = query.count()
        return failed_attempts >= max_attempts


class PasswordResetToken(models.Model):
    """
    Rastrea tokens de recuperación de contraseña
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Token de Recuperación'
        verbose_name_plural = 'Tokens de Recuperación'

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    def is_valid(self, expiry_hours=24):
        """
        Verifica si el token sigue siendo válido
        """
        if self.used_at:
            return False

        expiry_time = self.created_at + timedelta(hours=expiry_hours)
        return timezone.now() <= expiry_time


class SecurityEvent(models.Model):
    """
    Registra eventos de seguridad importantes
    """
    EVENT_TYPES = [
        ('login_success', 'Login Exitoso'),
        ('login_failed', 'Login Fallido'),
        ('password_reset_request', 'Solicitud de Reset de Contraseña'),
        ('password_reset_complete', 'Reset de Contraseña Completado'),
        ('password_changed', 'Contraseña Cambiada'),
        ('account_locked', 'Cuenta Bloqueada'),
        ('suspicious_activity', 'Actividad Sospechosa'),
        ('2fa_enabled', '2FA Habilitado'),
        ('2fa_disabled', '2FA Deshabilitado'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='security_events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, db_index=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Evento de Seguridad'
        verbose_name_plural = 'Eventos de Seguridad'
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['event_type', '-timestamp']),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else 'Anónimo'
        return f"{user_str} - {self.get_event_type_display()} - {self.timestamp}"


class SessionSecurity(models.Model):
    """
    Rastrea sesiones activas de usuarios
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='active_sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-last_activity']
        verbose_name = 'Sesión Activa'
        verbose_name_plural = 'Sesiones Activas'

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} - {self.last_activity}"

