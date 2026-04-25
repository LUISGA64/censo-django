"""
Vista de búsqueda global para CensoWeb
Permite buscar en Personas, Fichas Familiares y Documentos desde cualquier parte del sistema
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from .models import Person, FamilyCard

import logging

logger = logging.getLogger(__name__)


@login_required
def test_search_view(request):
    """Vista de prueba para debugging de búsqueda"""
    return render(request, 'test_search.html')


@login_required
def search_page_view(request):
    """Vista HTML para búsqueda global (página dedicada)"""
    return render(request, 'search_page.html')


@login_required
def global_search(request):
    """
    Búsqueda global en todo el sistema
    Busca en: Personas, Fichas Familiares, Documentos
    """
    query = request.GET.get('q', '').strip()

    # Validar longitud mínima
    if len(query) < 3:
        return JsonResponse({
            'error': 'Por favor ingrese al menos 3 caracteres',
            'total': 0
        }, status=400)

    # Obtener organización del usuario
    org = request.user_organization if hasattr(request, 'user_organization') else None

    # Inicializar resultados
    results = {
        'personas': [],
        'fichas': [],
        'documentos': [],
        'total': 0,
        'query': query
    }

    try:
        # ============================================
        # BUSCAR EN PERSONAS
        # ============================================
        personas_qs = Person.objects.filter(state=True)

        # Filtrar por organización si no es superuser
        if org and not request.user.is_superuser:
            personas_qs = personas_qs.filter(family_card__organization=org)

        # Aplicar búsqueda
        personas = personas_qs.filter(
            Q(first_name_1__icontains=query) |
            Q(first_name_2__icontains=query) |
            Q(last_name_1__icontains=query) |
            Q(last_name_2__icontains=query) |
            Q(identification_person__icontains=query)
        ).select_related('family_card', 'gender', 'document_type')[:8]

        for persona in personas:
            results['personas'].append({
                'id': persona.id,
                'name': persona.full_name,
                'identification': persona.identification_person,
                'document_type': persona.document_type.document_type if persona.document_type else '',
                'family_card_number': persona.family_card.family_card_number if persona.family_card else '',
                'gender': persona.gender.gender if persona.gender else '',
                'url': reverse('detail-person', kwargs={'pk': persona.id})
            })

        # ============================================
        # BUSCAR EN FICHAS FAMILIARES
        # ============================================
        fichas_qs = FamilyCard.objects.filter(state=True)

        # Filtrar por organización
        if org and not request.user.is_superuser:
            fichas_qs = fichas_qs.filter(organization=org)

        # Aplicar búsqueda
        fichas = fichas_qs.filter(
            Q(family_card_number__icontains=query) |
            Q(address_home__icontains=query) |
            Q(sidewalk_home__sidewalk_name__icontains=query)
        ).select_related('sidewalk_home', 'organization')[:8]

        for ficha in fichas:
            # Contar miembros
            members_count = Person.objects.filter(family_card=ficha, state=True).count()

            # Obtener cabeza de familia
            family_head = Person.objects.filter(
                family_card=ficha,
                family_head=True,
                state=True
            ).first()

            results['fichas'].append({
                'id': ficha.id,
                'number': ficha.family_card_number,
                'address': ficha.address_home or 'Sin dirección',
                'sidewalk': ficha.sidewalk_home.sidewalk_name if ficha.sidewalk_home else '',
                'members_count': members_count,
                'family_head': family_head.full_name if family_head else 'No definido',
                'url': f'/familia/{ficha.id}/'
            })

        # ============================================
        # BUSCAR EN DOCUMENTOS (si existe el modelo)
        # ============================================
        try:
            from .models import GeneratedDocument

            docs_qs = GeneratedDocument.objects.all()

            # Filtrar por organización
            if org and not request.user.is_superuser:
                docs_qs = docs_qs.filter(organization=org)

            # Aplicar búsqueda
            documentos = docs_qs.filter(
                Q(document_number__icontains=query) |
                Q(person__first_name_1__icontains=query) |
                Q(person__last_name_1__icontains=query) |
                Q(person__identification_person__icontains=query)
            ).select_related('person', 'document_type')[:8]

            for doc in documentos:
                from datetime import date
                is_expired = doc.expiration_date < date.today() if doc.expiration_date else False

                results['documentos'].append({
                    'id': doc.id,
                    'number': doc.document_number,
                    'person_name': doc.person.full_name if doc.person else '',
                    'document_type': doc.document_type.name if hasattr(doc, 'document_type') and doc.document_type else 'Documento',
                    'status': doc.status,
                    'is_expired': is_expired,
                    'url': reverse('view-document', kwargs={'document_id': doc.id})
                })

        except ImportError:
            # Modelo GeneratedDocument no existe aún
            logger.info("Modelo GeneratedDocument no disponible en búsqueda global")
            pass

        # Calcular total
        results['total'] = (
            len(results['personas']) +
            len(results['fichas']) +
            len(results['documentos'])
        )

        return JsonResponse(results)

    except Exception as e:
        logger.error(f"Error en búsqueda global: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'Error al realizar la búsqueda. Intente nuevamente.',
            'total': 0
        }, status=500)


@login_required
def search_suggestions(request):
    """
    Proporciona sugerencias rápidas para autocompletado
    Más rápido que global_search, solo retorna nombres
    """
    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        return JsonResponse({'suggestions': []})

    org = request.user_organization if hasattr(request, 'user_organization') else None
    suggestions = []

    try:
        # Buscar personas
        personas_qs = Person.objects.filter(state=True)
        if org and not request.user.is_superuser:
            personas_qs = personas_qs.filter(family_card__organization=org)

        personas = personas_qs.filter(
            Q(first_name_1__icontains=query) |
            Q(last_name_1__icontains=query) |
            Q(identification_person__icontains=query)
        )[:5]

        for p in personas:
            suggestions.append({
                'type': 'persona',
                'text': f"{p.full_name} - {p.identification_person}",
                'value': p.identification_person,
                'url': f'/persona/{p.id}/'
            })

        return JsonResponse({'suggestions': suggestions})

    except Exception as e:
        logger.error(f"Error en sugerencias: {str(e)}")
        return JsonResponse({'suggestions': []})
