"""
Vistas para el sistema de notificaciones
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Notification, NotificationPreference
from .notification_service import NotificationService


@login_required
def notifications_list(request):
    """Lista de todas las notificaciones del usuario"""
    notifications = Notification.objects.filter(
        user=request.user
    ).select_related(
        'organization', 'related_person', 'related_document', 'related_family'
    ).order_by('-created_at')

    # Paginación
    from django.core.paginator import Paginator
    paginator = Paginator(notifications, 20)  # 20 notificaciones por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Estadísticas
    total_count = notifications.count()
    unread_count = notifications.filter(is_read=False).count()

    context = {
        'page_obj': page_obj,
        'total_count': total_count,
        'unread_count': unread_count,
    }

    return render(request, 'notifications/list.html', context)


@login_required
def notification_detail(request, notification_id):
    """Detalle de una notificación y marcarla como leída"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    # Marcar como leída
    if not notification.is_read:
        notification.mark_as_read()

    # Redirigir al link si existe
    if notification.link:
        return redirect(notification.link)

    # Si no hay link, mostrar detalle
    context = {
        'notification': notification,
    }

    return render(request, 'notifications/detail.html', context)


@login_required
@require_POST
def mark_as_read(request, notification_id):
    """Marcar una notificación como leída (AJAX)"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    notification.mark_as_read()

    return JsonResponse({
        'success': True,
        'message': 'Notificación marcada como leída',
        'unread_count': NotificationService.get_unread_count(request.user)
    })


@login_required
@require_POST
def mark_all_as_read(request):
    """Marcar todas las notificaciones como leídas (AJAX)"""
    NotificationService.mark_all_as_read(request.user)

    return JsonResponse({
        'success': True,
        'message': 'Todas las notificaciones marcadas como leídas',
        'unread_count': 0
    })


@login_required
def notifications_unread(request):
    """Obtener notificaciones no leídas (AJAX para dropdown)"""
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).select_related(
        'organization', 'related_person', 'related_document', 'related_family'
    ).order_by('-created_at')[:10]  # Últimas 10 no leídas

    notifications_data = [{
        'id': notif.id,
        'title': notif.title,
        'message': notif.message,
        'icon': notif.get_icon(),
        'color': notif.get_color(),
        'link': notif.link,
        'created_at': notif.created_at.isoformat(),
        'time_ago': get_time_ago(notif.created_at),
    } for notif in notifications]

    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': NotificationService.get_unread_count(request.user),
        'total': notifications.count()
    })


@login_required
def notification_preferences(request):
    """Configuración de preferencias de notificaciones"""
    try:
        preferences = request.user.notification_preferences
    except NotificationPreference.DoesNotExist:
        preferences = NotificationPreference.objects.create(user=request.user)

    if request.method == 'POST':
        # Actualizar preferencias
        preferences.receive_email = request.POST.get('receive_email') == 'on'
        preferences.receive_inapp = request.POST.get('receive_inapp') == 'on'

        preferences.notify_document_expiring = request.POST.get('notify_document_expiring') == 'on'
        preferences.notify_document_expired = request.POST.get('notify_document_expired') == 'on'
        preferences.notify_document_generated = request.POST.get('notify_document_generated') == 'on'
        preferences.notify_person_created = request.POST.get('notify_person_created') == 'on'
        preferences.notify_family_created = request.POST.get('notify_family_created') == 'on'
        preferences.notify_system_updates = request.POST.get('notify_system_updates') == 'on'
        preferences.notify_security_alerts = request.POST.get('notify_security_alerts') == 'on'

        preferences.email_frequency = request.POST.get('email_frequency', 'INSTANT')

        preferences.save()

        messages.success(request, 'Preferencias de notificaciones actualizadas correctamente.')
        return redirect('notification_preferences')

    context = {
        'preferences': preferences,
    }

    return render(request, 'notifications/preferences.html', context)


@login_required
@require_POST
def delete_notification(request, notification_id):
    """Eliminar una notificación"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    notification.delete()

    return JsonResponse({
        'success': True,
        'message': 'Notificación eliminada',
        'unread_count': NotificationService.get_unread_count(request.user)
    })


# Funciones auxiliares

def get_time_ago(dt):
    """
    Retorna el tiempo transcurrido en formato legible.

    Args:
        dt: datetime

    Returns:
        str: Tiempo transcurrido (ej: "hace 5 minutos")
    """
    from django.utils import timezone
    from datetime import timedelta

    now = timezone.now()
    diff = now - dt

    seconds = diff.total_seconds()

    if seconds < 60:
        return "hace un momento"
    elif seconds < 3600:  # menos de 1 hora
        minutes = int(seconds / 60)
        return f"hace {minutes} minuto{'s' if minutes > 1 else ''}"
    elif seconds < 86400:  # menos de 1 día
        hours = int(seconds / 3600)
        return f"hace {hours} hora{'s' if hours > 1 else ''}"
    elif seconds < 604800:  # menos de 1 semana
        days = int(seconds / 86400)
        return f"hace {days} día{'s' if days > 1 else ''}"
    elif seconds < 2592000:  # menos de 30 días
        weeks = int(seconds / 604800)
        return f"hace {weeks} semana{'s' if weeks > 1 else ''}"
    else:
        return dt.strftime('%d/%m/%Y')
