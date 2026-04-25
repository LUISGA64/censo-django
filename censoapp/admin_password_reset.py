"""
Sistema de recuperación de contraseñas para aplicaciones privadas
Opción 1: Solo administradores pueden restablecer contraseñas
Opción 2: Notificación al admin cuando un usuario solicita recuperación
"""
from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required


class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin personalizado de User con funcionalidad de reset de contraseña
    """
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'last_login', 'reset_password_button']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'last_login']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-last_login']

    fieldsets = (
        ('Información de Usuario', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['last_login', 'date_joined']

    def reset_password_button(self, obj):
        """Botón para restablecer contraseña del usuario"""
        return format_html(
            '<a class="button" href="{}">🔑 Restablecer Contraseña</a>',
            f'/admin/auth/user/{obj.pk}/reset-password/'
        )
    reset_password_button.short_description = 'Acciones'

    def get_urls(self):
        """Agregar URL personalizada para reset de contraseña"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/reset-password/',
                self.admin_site.admin_view(self.reset_password_view),
                name='auth_user_reset_password',
            ),
        ]
        return custom_urls + urls

    def reset_password_view(self, request, user_id):
        """Vista para que admin restablezca contraseña de usuario"""
        user = User.objects.get(pk=user_id)

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, 'Las contraseñas no coinciden.')
            elif len(new_password) < 12:
                messages.error(request, 'La contraseña debe tener al menos 12 caracteres.')
            else:
                # Cambiar contraseña
                user.set_password(new_password)
                user.save()

                # Registrar evento de seguridad
                from censoapp.security_models import SecurityEvent
                SecurityEvent.objects.create(
                    user=user,
                    event_type='password_changed',
                    description=f'Contraseña restablecida por administrador {request.user.username}',
                    ip_address=self._get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    metadata={
                        'reset_by': request.user.username,
                        'reset_by_id': request.user.id
                    }
                )

                # Enviar email al usuario (opcional)
                if user.email:
                    try:
                        send_mail(
                            subject='[Censo Web] Tu contraseña ha sido restablecida',
                            message=f'''Hola {user.first_name or user.username},

Tu contraseña ha sido restablecida por un administrador.

Tu nueva contraseña temporal es: {new_password}

Por favor, cámbiala inmediatamente después de iniciar sesión.

Saludos,
Equipo de Censo Web''',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[user.email],
                            fail_silently=True,
                        )
                        messages.success(request, f'Contraseña restablecida exitosamente. Email enviado a {user.email}.')
                    except Exception as e:
                        messages.warning(request, f'Contraseña restablecida, pero no se pudo enviar el email: {e}')
                else:
                    messages.success(request, f'Contraseña restablecida exitosamente. Comunica al usuario su nueva contraseña: {new_password}')

                return redirect('admin:auth_user_changelist')

        context = {
            'title': f'Restablecer contraseña de {user.username}',
            'user_obj': user,
            'opts': self.model._meta,
            'has_view_permission': True,
        }

        return render(request, 'admin/auth/user/reset_password.html', context)

    def _get_client_ip(self, request):
        """Obtener IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


