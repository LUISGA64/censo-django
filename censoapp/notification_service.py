"""
Servicio de Notificaciones para Censo Web
Maneja el envío de notificaciones in-app y por email
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, date
from .models import (
    Notification, NotificationPreference, NotificationType,
    GeneratedDocument, Person, FamilyCard, User
)


class NotificationService:
    """Servicio principal para gestión de notificaciones"""

    @staticmethod
    def create_notification(
        user,
        title,
        message,
        notification_type=NotificationType.CUSTOM,
        link=None,
        organization=None,
        related_person=None,
        related_document=None,
        related_family=None,
        send_email=False
    ):
        """
        Crea una notificación in-app y opcionalmente envía email.

        Args:
            user: Usuario destinatario
            title: Título de la notificación
            message: Mensaje de la notificación
            notification_type: Tipo de notificación
            link: URL para redireccionar
            organization: Organización relacionada
            related_person: Persona relacionada
            related_document: Documento relacionado
            related_family: Ficha familiar relacionada
            send_email: Si se debe enviar email

        Returns:
            Notification: La notificación creada
        """
        # Verificar preferencias del usuario
        try:
            prefs = user.notification_preferences
        except NotificationPreference.DoesNotExist:
            prefs = NotificationPreference.objects.create(user=user)

        # Crear notificación in-app si el usuario lo permite
        notification = None
        if prefs.receive_inapp:
            notification = Notification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                link=link,
                organization=organization,
                related_person=related_person,
                related_document=related_document,
                related_family=related_family
            )

        # Enviar email si se solicita y el usuario lo permite
        if send_email and prefs.receive_email and prefs.email_frequency == 'INSTANT':
            NotificationService.send_email_notification(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                link=link,
                notification=notification
            )

            if notification:
                notification.sent_email = True
                notification.email_sent_at = timezone.now()
                notification.save(update_fields=['sent_email', 'email_sent_at'])

        return notification

    @staticmethod
    def send_email_notification(user, title, message, notification_type=None, link=None, notification=None):
        """
        Envía una notificación por email.

        Args:
            user: Usuario destinatario
            title: Título del email
            message: Mensaje del email
            notification_type: Tipo de notificación
            link: URL para ver más detalles
            notification: Instancia de notificación (opcional)
        """
        try:
            # Preparar contexto para el template
            context = {
                'user': user,
                'title': title,
                'message': message,
                'notification_type': notification_type,
                'link': link,
                'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
                'site_name': settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'Censo Web',
            }

            # Renderizar email HTML
            html_message = render_to_string('emails/notification.html', context)
            plain_message = strip_tags(html_message)

            # Configurar email
            from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else settings.EMAIL_HOST_USER
            recipient_list = [user.email] if user.email else []

            if recipient_list:
                # Crear email con HTML
                email = EmailMultiAlternatives(
                    subject=f'[Censo Web] {title}',
                    body=plain_message,
                    from_email=from_email,
                    to=recipient_list
                )
                email.attach_alternative(html_message, "text/html")
                email.send()

                return True
        except Exception as e:
            print(f"Error enviando email: {e}")
            return False

        return False

    @staticmethod
    def notify_document_expiring(document, days_before=30):
        """
        Notifica sobre documentos próximos a vencer.

        Args:
            document: Instancia de GeneratedDocument
            days_before: Días antes del vencimiento para notificar
        """
        if not document.expiration_date:
            return

        days_until_expiration = (document.expiration_date - date.today()).days

        if days_until_expiration <= days_before and days_until_expiration > 0:
            # Notificar al usuario que creó el documento
            if document.created_by:
                title = f"Documento próximo a vencer"
                message = (
                    f"El documento {document.document_type.document_type_name} "
                    f"No. {document.document_number} para {document.person.full_name} "
                    f"vencerá en {days_until_expiration} días ({document.expiration_date.strftime('%d/%m/%Y')})."
                )

                NotificationService.create_notification(
                    user=document.created_by,
                    title=title,
                    message=message,
                    notification_type=NotificationType.DOCUMENT_EXPIRING,
                    link=f"/documents/{document.id}/",
                    organization=document.organization,
                    related_document=document,
                    related_person=document.person,
                    send_email=True
                )

    @staticmethod
    def notify_document_expired(document):
        """
        Notifica sobre documentos vencidos.

        Args:
            document: Instancia de GeneratedDocument
        """
        if document.is_expired:
            if document.created_by:
                title = f"Documento vencido"
                message = (
                    f"El documento {document.document_type.document_type_name} "
                    f"No. {document.document_number} para {document.person.full_name} "
                    f"ha vencido ({document.expiration_date.strftime('%d/%m/%Y')})."
                )

                NotificationService.create_notification(
                    user=document.created_by,
                    title=title,
                    message=message,
                    notification_type=NotificationType.DOCUMENT_EXPIRED,
                    link=f"/documents/{document.id}/",
                    organization=document.organization,
                    related_document=document,
                    related_person=document.person,
                    send_email=True
                )

    @staticmethod
    def notify_document_generated(document, user):
        """
        Notifica sobre un documento generado.

        Args:
            document: Instancia de GeneratedDocument
            user: Usuario a notificar
        """
        title = f"Documento generado exitosamente"
        message = (
            f"Se ha generado el documento {document.document_type.document_type_name} "
            f"No. {document.document_number} para {document.person.full_name}."
        )

        NotificationService.create_notification(
            user=user,
            title=title,
            message=message,
            notification_type=NotificationType.DOCUMENT_GENERATED,
            link=f"/documents/{document.id}/",
            organization=document.organization,
            related_document=document,
            related_person=document.person,
            send_email=False  # No enviar email para documentos generados por defecto
        )

    @staticmethod
    def notify_person_created(person, user):
        """
        Notifica sobre una persona creada.

        Args:
            person: Instancia de Person
            user: Usuario a notificar
        """
        title = f"Nueva persona registrada"
        message = (
            f"Se ha registrado a {person.full_name} "
            f"en la ficha familiar {person.family_card.family_card_number}."
        )

        NotificationService.create_notification(
            user=user,
            title=title,
            message=message,
            notification_type=NotificationType.PERSON_CREATED,
            link=f"/persons/{person.id}/",
            organization=person.family_card.organization,
            related_person=person,
            related_family=person.family_card,
            send_email=False
        )

    @staticmethod
    def notify_family_created(family_card, user):
        """
        Notifica sobre una ficha familiar creada.

        Args:
            family_card: Instancia de FamilyCard
            user: Usuario a notificar
        """
        title = f"Nueva ficha familiar registrada"
        message = (
            f"Se ha registrado la ficha familiar No. {family_card.family_card_number} "
            f"en {family_card.sidewalk_home.sidewalk_name}."
        )

        NotificationService.create_notification(
            user=user,
            title=title,
            message=message,
            notification_type=NotificationType.FAMILY_CREATED,
            link=f"/families/{family_card.id}/",
            organization=family_card.organization,
            related_family=family_card,
            send_email=False
        )

    @staticmethod
    def check_expiring_documents():
        """
        Verifica documentos próximos a vencer y envía notificaciones.
        Este método se debe ejecutar diariamente (via cron o celery).
        """
        today = date.today()
        days_to_check = [30, 15, 7, 3, 1]  # Notificar en estos días antes del vencimiento

        for days in days_to_check:
            expiration_date = today + timedelta(days=days)

            # Buscar documentos que vencen en exactamente N días
            documents = GeneratedDocument.objects.filter(
                status='ISSUED',
                expiration_date=expiration_date
            ).select_related('person', 'organization', 'created_by', 'document_type')

            for doc in documents:
                NotificationService.notify_document_expiring(doc, days)

        # Notificar documentos vencidos (último día)
        expired_docs = GeneratedDocument.objects.filter(
            status='ISSUED',
            expiration_date__lt=today
        ).select_related('person', 'organization', 'created_by', 'document_type')

        for doc in expired_docs:
            NotificationService.notify_document_expired(doc)
            # Actualizar estado a vencido
            doc.status = 'EXPIRED'
            doc.save(update_fields=['status'])

    @staticmethod
    def get_unread_count(user):
        """
        Obtiene el número de notificaciones no leídas para un usuario.

        Args:
            user: Usuario

        Returns:
            int: Número de notificaciones no leídas
        """
        return Notification.objects.filter(user=user, is_read=False).count()

    @staticmethod
    def get_recent_notifications(user, limit=10):
        """
        Obtiene las notificaciones recientes de un usuario.

        Args:
            user: Usuario
            limit: Número máximo de notificaciones

        Returns:
            QuerySet: Notificaciones recientes
        """
        return Notification.objects.filter(user=user).select_related(
            'organization', 'related_person', 'related_document', 'related_family'
        )[:limit]

    @staticmethod
    def mark_all_as_read(user):
        """
        Marca todas las notificaciones de un usuario como leídas.

        Args:
            user: Usuario
        """
        Notification.objects.filter(user=user, is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )

    @staticmethod
    def delete_old_notifications(days=30):
        """
        Elimina notificaciones leídas antiguas.

        Args:
            days: Días de antigüedad para eliminar
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        deleted_count = Notification.objects.filter(
            is_read=True,
            read_at__lt=cutoff_date
        ).delete()[0]

        return deleted_count


# Función auxiliar para templates
def get_user_notifications(user, limit=5):
    """
    Función auxiliar para usar en templates.

    Args:
        user: Usuario
        limit: Número de notificaciones

    Returns:
        dict: Diccionario con notificaciones y conteo
    """
    return {
        'notifications': NotificationService.get_recent_notifications(user, limit),
        'unread_count': NotificationService.get_unread_count(user),
    }
