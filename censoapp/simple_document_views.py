"""
Vistas simplificadas para generación de documentos con jsPDF.
Sistema simple sin dependencia del administrador de plantillas.
Incluye generación de QR y guardado en BD.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from censoapp.models import Person, Organizations, BoardPosition, GeneratedDocument, DocumentType
from datetime import datetime, timedelta
import hashlib
import logging

logger = logging.getLogger(__name__)


def generate_verification_hash(document_id, person_id, document_type_name, timestamp):
    """
    Genera un hash único para verificación del documento.
    """
    data = f"{document_id}_{person_id}_{document_type_name}_{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()


@login_required
def select_document_type(request, person_id):
    """
    Vista para seleccionar el tipo de documento a generar.
    """
    person = get_object_or_404(Person, pk=person_id)

    # Verificar permisos de organización
    if not request.user.is_superuser:
        try:
            user_profile = request.user.userprofile
            if person.family_card.organization != user_profile.organization:
                messages.error(request, 'No tiene permisos para generar documentos para esta persona.')
                return redirect('detail-person', pk=person_id)
        except AttributeError:
            messages.error(request, 'No tiene un perfil de usuario configurado.')
            return redirect('home')

    context = {
        'person': person,
        'segment': 'personas'
    }

    return render(request, 'censo/documentos/select_document_type.html', context)


@login_required
def generate_aval_general(request, person_id):
    """
    Generar AVAL GENERAL con campos: entidad, motivo, cargo
    Guarda en BD y genera QR de verificación
    """
    person = get_object_or_404(Person, pk=person_id)
    organization = person.family_card.organization

    # Verificar permisos
    if not request.user.is_superuser:
        try:
            user_profile = request.user.userprofile
            if organization != user_profile.organization:
                messages.error(request, 'No tiene permisos para generar documentos para esta persona.')
                return redirect('detail-person', pk=person_id)
        except AttributeError:
            messages.error(request, 'No tiene un perfil de usuario configurado.')
            return redirect('home')

    # Obtener junta directiva vigente
    signers = BoardPosition.objects.filter(
        organization=organization,
        is_active=True
    ).select_related('holder_person')

    if not signers.exists():
        messages.error(request, 'No hay junta directiva vigente para firmar documentos.')
        return redirect('detail-person', pk=person_id)

    # Si es POST, crear el documento en BD
    documento_generado = None
    if request.method == 'POST':
        try:
            # Obtener o crear tipo de documento "Aval General"
            document_type, created = DocumentType.objects.get_or_create(
                document_type_name='Aval General',
                defaults={'is_active': True, 'requires_expiration': False}
            )

            # Si ya existía, asegurarse de que no requiera vencimiento
            if not created and document_type.requires_expiration:
                document_type.requires_expiration = False
                document_type.save()

            # Obtener datos del formulario
            entidad = request.POST.get('entidad', '')
            motivo = request.POST.get('motivo', '')
            cargo = request.POST.get('cargo', '')

            # Crear contenido del documento
            content = f"AVAL GENERAL para {person.full_name} - Entidad: {entidad}, Motivo: {motivo}, Cargo: {cargo}"

            # Calcular fecha de vencimiento (1 año desde emisión)
            issue_date = datetime.now().date()
            expiration_date = issue_date + timedelta(days=365)

            # Crear documento en BD
            documento_generado = GeneratedDocument.objects.create(
                document_type=document_type,
                person=person,
                organization=organization,
                document_content=content,
                issue_date=issue_date,
                expiration_date=expiration_date,
                status='ISSUED'
            )

            # Agregar firmantes
            documento_generado.signers.set(signers)

            # Generar hash de verificación
            timestamp = datetime.now().timestamp()
            verification_hash = generate_verification_hash(
                documento_generado.id,
                person.id,
                'Aval General',
                timestamp
            )
            documento_generado.verification_hash = verification_hash
            documento_generado.save()

            logger.info(f"Documento Aval General #{documento_generado.document_number} generado para {person.full_name}")

        except Exception as e:
            logger.error(f"Error al guardar documento: {e}")
            messages.error(request, f"Error al guardar el documento: {str(e)}")

    context = {
        'person': person,
        'organization': organization,
        'signers': signers,
        'segment': 'personas',
        'documento_generado': documento_generado
    }

    return render(request, 'censo/documentos/aval_general.html', context)


@login_required
def generate_aval_estudio(request, person_id):
    """
    Generar AVAL DE ESTUDIO con campos: entidad, programa, semestre, proyecto, horas
    Guarda en BD y genera QR de verificación
    """
    person = get_object_or_404(Person, pk=person_id)
    organization = person.family_card.organization

    # Verificar permisos
    if not request.user.is_superuser:
        try:
            user_profile = request.user.userprofile
            if organization != user_profile.organization:
                messages.error(request, 'No tiene permisos para generar documentos para esta persona.')
                return redirect('detail-person', pk=person_id)
        except AttributeError:
            messages.error(request, 'No tiene un perfil de usuario configurado.')
            return redirect('home')

    # Obtener junta directiva vigente
    signers = BoardPosition.objects.filter(
        organization=organization,
        is_active=True
    ).select_related('holder_person')

    if not signers.exists():
        messages.error(request, 'No hay junta directiva vigente para firmar documentos.')
        return redirect('detail-person', pk=person_id)

    # Si es POST, crear el documento en BD
    documento_generado = None
    if request.method == 'POST':
        try:
            # Obtener o crear tipo de documento "Aval de Estudio"
            document_type, created = DocumentType.objects.get_or_create(
                document_type_name='Aval de Estudio',
                defaults={'is_active': True, 'requires_expiration': False}
            )

            # Si ya existía, asegurarse de que no requiera vencimiento
            if not created and document_type.requires_expiration:
                document_type.requires_expiration = False
                document_type.save()

            # Obtener datos del formulario
            entidad = request.POST.get('entidad', '')
            programa = request.POST.get('programa', '')
            semestre = request.POST.get('semestre', '')
            proyecto = request.POST.get('proyecto', '')
            horas = request.POST.get('horas', '')

            # Crear contenido del documento
            content = f"AVAL DE ESTUDIO para {person.full_name} - Institución: {entidad}, Programa: {programa}, Semestre: {semestre}"
            if proyecto:
                content += f", Proyecto: {proyecto}"
            if horas:
                content += f", Horas: {horas}"

            # Calcular fecha de vencimiento (1 año desde emisión)
            issue_date = datetime.now().date()
            expiration_date = issue_date + timedelta(days=365)

            # Crear documento en BD
            documento_generado = GeneratedDocument.objects.create(
                document_type=document_type,
                person=person,
                organization=organization,
                document_content=content,
                issue_date=issue_date,
                expiration_date=expiration_date,
                status='ISSUED'
            )

            # Agregar firmantes
            documento_generado.signers.set(signers)

            # Generar hash de verificación
            timestamp = datetime.now().timestamp()
            verification_hash = generate_verification_hash(
                documento_generado.id,
                person.id,
                'Aval de Estudio',
                timestamp
            )
            documento_generado.verification_hash = verification_hash
            documento_generado.save()

            logger.info(f"Documento Aval de Estudio #{documento_generado.document_number} generado para {person.full_name}")

        except Exception as e:
            logger.error(f"Error al guardar documento: {e}")
            messages.error(request, f"Error al guardar el documento: {str(e)}")

    context = {
        'person': person,
        'organization': organization,
        'signers': signers,
        'segment': 'personas',
        'documento_generado': documento_generado
    }

    return render(request, 'censo/documentos/aval_estudio.html', context)


@login_required
def generate_constancia_pertenencia(request, person_id):
    """
    Generar CONSTANCIA DE PERTENENCIA (sin campos adicionales)
    Guarda en BD y genera QR de verificación
    """
    person = get_object_or_404(Person, pk=person_id)
    organization = person.family_card.organization

    # Verificar permisos
    if not request.user.is_superuser:
        try:
            user_profile = request.user.userprofile
            if organization != user_profile.organization:
                messages.error(request, 'No tiene permisos para generar documentos para esta persona.')
                return redirect('detail-person', pk=person_id)
        except AttributeError:
            messages.error(request, 'No tiene un perfil de usuario configurado.')
            return redirect('home')

    # Obtener junta directiva vigente
    signers = BoardPosition.objects.filter(
        organization=organization,
        is_active=True
    ).select_related('holder_person')

    if not signers.exists():
        messages.error(request, 'No hay junta directiva vigente para firmar documentos.')
        return redirect('detail-person', pk=person_id)

    # Crear el documento en BD automáticamente
    try:
        # Obtener o crear tipo de documento "Constancia de Pertenencia"
        document_type, created = DocumentType.objects.get_or_create(
            document_type_name='Constancia de Pertenencia',
            defaults={'is_active': True, 'requires_expiration': False}
        )

        # Si ya existía, asegurarse de que no requiera vencimiento
        if not created and document_type.requires_expiration:
            document_type.requires_expiration = False
            document_type.save()

        # Crear contenido del documento
        content = f"CONSTANCIA DE PERTENENCIA para {person.full_name} - Resguardo: {organization.organization_name}, Vereda: {person.family_card.sidewalk_home.sidewalk_name}"

        # Calcular fecha de vencimiento (1 año desde emisión)
        issue_date = datetime.now().date()
        expiration_date = issue_date + timedelta(days=365)

        # Crear documento en BD
        documento_generado = GeneratedDocument.objects.create(
            document_type=document_type,
            person=person,
            organization=organization,
            document_content=content,
            issue_date=issue_date,
            expiration_date=expiration_date,
            status='ISSUED'
        )

        # Agregar firmantes
        documento_generado.signers.set(signers)

        # Generar hash de verificación
        timestamp = datetime.now().timestamp()
        verification_hash = generate_verification_hash(
            documento_generado.id,
            person.id,
            'Constancia de Pertenencia',
            timestamp
        )
        documento_generado.verification_hash = verification_hash
        documento_generado.save()

        logger.info(f"Documento Constancia de Pertenencia #{documento_generado.document_number} generado para {person.full_name}")

    except Exception as e:
        logger.error(f"Error al guardar documento: {e}")
        messages.error(request, f"Error al guardar el documento: {str(e)}")
        documento_generado = None

    context = {
        'person': person,
        'organization': organization,
        'signers': signers,
        'segment': 'personas',
        'documento_generado': documento_generado
    }

    return render(request, 'censo/documentos/constancia_pertenencia.html', context)

