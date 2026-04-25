"""
Vista personalizada para solicitud de recuperación de contraseña
en aplicaciones privadas - Notifica al administrador en lugar de enviar
al usuario directamente
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from censoapp.security_models import SecurityEvent


def get_client_ip(request):
    """Obtener IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def password_reset_request_to_admin(request):
    """
    Vista para solicitar recuperación de contraseña
    Envía notificación al administrador en lugar de al usuario
    """
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email', '').strip()
        reason = request.POST.get('reason', '').strip()
        contact_info = request.POST.get('contact_info', '').strip()

        if not username_or_email:
            messages.error(request, 'Por favor ingresa tu usuario o email.')
            return render(request, 'account/password_reset_request_admin.html')

        # Buscar usuario
        user = None
        try:
            # Intentar por username
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                # Intentar por email
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                pass

        # Por seguridad, siempre mostrar el mismo mensaje
        # (no revelar si el usuario existe o no)

        if user:
            # Registrar evento de seguridad
            SecurityEvent.objects.create(
                user=user,
                event_type='password_reset_request',
                description=f'Solicitud de recuperación de contraseña - Razón: {reason}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                metadata={
                    'contact_info': contact_info,
                    'reason': reason,
                }
            )

            # Enviar email al administrador
            import logging
            logger = logging.getLogger(__name__)

            try:
                # Obtener emails de administradores
                admin_emails = User.objects.filter(
                    is_superuser=True,
                    is_active=True,
                    email__isnull=False
                ).exclude(email='').values_list('email', flat=True)

                if admin_emails:
                    admin_emails_list = list(admin_emails)
                    logger.info(f'Enviando email de recuperación a {len(admin_emails_list)} administradores: {admin_emails_list}')

                    email_sent = send_mail(
                        subject='[Censo Web - ADMIN] Solicitud de Recuperación de Contraseña',
                        message=f'''Solicitud de Recuperación de Contraseña

Un usuario ha solicitado recuperación de contraseña.

DATOS DEL USUARIO:
------------------
Usuario: {user.username}
Nombre: {user.first_name} {user.last_name}
Email: {user.email or 'No configurado'}
Último login: {user.last_login or 'Nunca'}

DATOS DE LA SOLICITUD:
----------------------
Razón: {reason or 'No especificada'}
Información de contacto: {contact_info or 'No especificada'}
IP de solicitud: {get_client_ip(request)}
Fecha/Hora: {SecurityEvent.objects.filter(user=user).latest('timestamp').timestamp}

ACCIÓN REQUERIDA:
-----------------
1. Verificar la identidad del usuario (presencialmente, por teléfono, etc.)
2. Si es válido, ir a: {settings.SITE_URL}/admin/auth/user/{user.id}/reset-password/
3. Restablecer la contraseña
4. Comunicar la nueva contraseña al usuario de forma segura

Este es un mensaje automático del sistema Censo Web.
No responder a este email.
''',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=admin_emails_list,
                        fail_silently=False,
                    )

                    if email_sent:
                        logger.info(f'Email enviado exitosamente a {admin_emails_list}')
                        # En desarrollo, mostrar mensaje adicional
                        if settings.DEBUG:
                            messages.info(
                                request,
                                f'[DEBUG] Email enviado a: {", ".join(admin_emails_list)}'
                            )
                    else:
                        logger.warning('send_mail retornó 0 - email no enviado')
                        if settings.DEBUG:
                            messages.warning(request, '[DEBUG] El email no fue enviado (send_mail retornó 0)')
                else:
                    logger.warning('No hay superusuarios con email configurado')
                    if settings.DEBUG:
                        messages.warning(
                            request,
                            '[DEBUG] No hay administradores con email configurado para recibir la notificación'
                        )

            except Exception as e:
                logger.error(f'Error enviando email a admin: {e}', exc_info=True)
                # En desarrollo, mostrar el error
                if settings.DEBUG:
                    messages.error(
                        request,
                        f'[DEBUG] Error al enviar email: {str(e)}'
                    )

        # Siempre mostrar el mismo mensaje (por seguridad)
        messages.success(
            request,
            'Tu solicitud ha sido enviada al administrador. '
            'Serás contactado pronto para verificar tu identidad y restablecer tu contraseña.'
        )

        return redirect('account_login')

    return render(request, 'account/password_reset_request_admin.html')


