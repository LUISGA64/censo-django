"""
Vistas para gestión de organizaciones y junta directiva
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from datetime import date

from .models import Organizations, BoardPosition, Person, Sidewalks
from .forms import OrganizationForm, BoardPositionForm, VeredaForm


def is_admin_or_superuser(user):
    """Verificar si el usuario es superuser o admin de organización"""
    return user.is_superuser or (
        hasattr(user, 'profile') and 
        user.profile.role in ['ADMIN'] and 
        user.profile.can_view_all_organizations
    )


@login_required
def organization_manage(request, pk):
    """
    Vista mejorada para gestionar una organización:
    - Ver detalles
    - Editar información
    - Gestionar junta directiva
    """
    organization = get_object_or_404(Organizations, pk=pk)
    
    # Verificar permisos
    if not request.user.is_superuser:
        user_profile = getattr(request, 'user_profile', None)
        if not user_profile or user_profile.organization != organization:
            messages.error(request, "No tiene permisos para gestionar esta organización.")
            return redirect('association')
    
    # Obtener junta directiva vigente
    today = date.today()
    current_board = BoardPosition.objects.filter(
        organization=organization,
        is_active=True,
        start_date__lte=today
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=today)
    ).select_related('holder_person', 'alternate_person').order_by('position_name')
    
    # Obtener firmantes autorizados
    signers = current_board.filter(can_sign_documents=True)
    
    # Estadísticas de la organización
    from .models import FamilyCard, Sidewalks
    total_fichas = FamilyCard.objects.filter(organization=organization, state=True).count()
    total_personas = Person.objects.filter(
        family_card__organization=organization,
        state=True
    ).count()
    total_veredas = Sidewalks.objects.filter(organization_id=organization).count()
    
    # Obtener veredas de la organización
    veredas = Sidewalks.objects.filter(
        organization_id=organization
    ).prefetch_related('familycard_set').order_by('sidewalk_name')

    context = {
        'organization': organization,
        'current_board': current_board,
        'signers': signers,
        'has_active_board': current_board.exists(),
        'total_fichas': total_fichas,
        'total_personas': total_personas,
        'total_veredas': total_veredas,
        'veredas': veredas,
        'segment': 'organization'
    }
    
    return render(request, 'censo/organizacion/organization_manage.html', context)


@login_required
@user_passes_test(is_admin_or_superuser, login_url='home')
def organization_edit(request, pk):
    """Editar información de la organización"""
    organization = get_object_or_404(Organizations, pk=pk)
    
    # Verificar permisos adicionales para no-superuser
    if not request.user.is_superuser:
        user_profile = getattr(request, 'user_profile', None)
        if not user_profile or user_profile.organization != organization:
            messages.error(request, "No tiene permisos para editar esta organización.")
            return redirect('organization_manage', pk=pk)
    
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()
            messages.success(request, f'Organización "{organization.organization_name}" actualizada correctamente.')
            return redirect('organization_manage', pk=pk)
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = OrganizationForm(instance=organization)
    
    context = {
        'form': form,
        'organization': organization,
        'action': 'edit',
        'segment': 'organization'
    }
    
    return render(request, 'censo/organizacion/organization_form.html', context)


@login_required
@user_passes_test(is_admin_or_superuser, login_url='home')
def board_position_create(request, organization_pk):
    """Crear un nuevo cargo en la junta directiva"""
    organization = get_object_or_404(Organizations, pk=organization_pk)
    
    # Verificar permisos
    if not request.user.is_superuser:
        user_profile = getattr(request, 'user_profile', None)
        if not user_profile or user_profile.organization != organization:
            messages.error(request, "No tiene permisos para gestionar esta organización.")
            return redirect('organization_manage', pk=organization_pk)
    
    if request.method == 'POST':
        form = BoardPositionForm(request.POST, organization=organization)
        if form.is_valid():
            board_position = form.save(commit=False)
            board_position.organization = organization
            try:
                board_position.save()
                messages.success(
                    request, 
                    f'Cargo "{board_position.get_position_name_display()}" creado correctamente.'
                )
                return redirect('organization_manage', pk=organization_pk)
            except Exception as e:
                messages.error(request, f'Error al crear el cargo: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = BoardPositionForm(organization=organization)
    
    context = {
        'form': form,
        'organization': organization,
        'action': 'create',
        'segment': 'organization'
    }
    
    return render(request, 'censo/organizacion/board_position_form.html', context)


@login_required
@user_passes_test(is_admin_or_superuser, login_url='home')
def board_position_edit(request, pk):
    """Editar un cargo de la junta directiva"""
    board_position = get_object_or_404(BoardPosition, pk=pk)
    organization = board_position.organization
    
    # Verificar permisos
    if not request.user.is_superuser:
        user_profile = getattr(request, 'user_profile', None)
        if not user_profile or user_profile.organization != organization:
            messages.error(request, "No tiene permisos para editar este cargo.")
            return redirect('organization_manage', pk=organization.pk)
    
    if request.method == 'POST':
        form = BoardPositionForm(
            request.POST, 
            instance=board_position,
            organization=organization
        )
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request, 
                    f'Cargo "{board_position.get_position_name_display()}" actualizado correctamente.'
                )
                return redirect('organization_manage', pk=organization.pk)
            except Exception as e:
                messages.error(request, f'Error al actualizar el cargo: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = BoardPositionForm(instance=board_position, organization=organization)
    
    context = {
        'form': form,
        'board_position': board_position,
        'organization': organization,
        'action': 'edit',
        'segment': 'organization'
    }
    
    return render(request, 'censo/organizacion/board_position_form.html', context)


@login_required
@user_passes_test(is_admin_or_superuser, login_url='home')
def board_position_delete(request, pk):
    """Eliminar/desactivar un cargo de la junta directiva"""
    board_position = get_object_or_404(BoardPosition, pk=pk)
    organization = board_position.organization
    
    # Verificar permisos
    if not request.user.is_superuser:
        user_profile = getattr(request, 'user_profile', None)
        if not user_profile or user_profile.organization != organization:
            messages.error(request, "No tiene permisos para eliminar este cargo.")
            return redirect('organization_manage', pk=organization.pk)
    
    if request.method == 'POST':
        cargo_nombre = board_position.get_position_name_display()
        titular = board_position.holder_person.full_name if board_position.holder_person else "Sin titular"
        
        # En lugar de eliminar, desactivar
        board_position.is_active = False
        board_position.end_date = date.today()
        board_position.save()
        
        messages.success(
            request, 
            f' Cargo "{cargo_nombre}" de {titular} desactivado correctamente.'
        )
        return redirect('organization_manage', pk=organization.pk)
    
    context = {
        'board_position': board_position,
        'organization': organization,
        'segment': 'organization'
    }
    
    return render(request, 'censo/organizacion/board_position_confirm_delete.html', context)


@login_required
def board_history(request, organization_pk):
    """Ver historial completo de la junta directiva"""
    organization = get_object_or_404(Organizations, pk=organization_pk)
    
    # Verificar permisos
    if not request.user.is_superuser:
        user_profile = getattr(request, 'user_profile', None)
        if not user_profile or user_profile.organization != organization:
            messages.error(request, "No tiene permisos para ver esta información.")
            return redirect('association')
    
    # Obtener todo el historial
    all_boards = BoardPosition.objects.filter(
        organization=organization
    ).select_related('holder_person', 'alternate_person').order_by('-start_date', 'position_name')
    
    # Paginación
    paginator = Paginator(all_boards, 20)  # 20 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'organization': organization,
        'page_obj': page_obj,
        'all_boards': page_obj,  # Para compatibilidad
        'segment': 'organization'
    }
    
    return render(request, 'censo/organizacion/board_history.html', context)


# ===== VEREDAS =====

@login_required
@user_passes_test(is_admin_or_superuser, login_url='home')
def vereda_create(request, organization_pk):
    """Crear una nueva vereda"""
    organization = get_object_or_404(Organizations, pk=organization_pk)

    # Verificar permisos
    if not request.user.is_superuser:
        user_profile = getattr(request, 'user_profile', None)
        if not user_profile or user_profile.organization != organization:
            messages.error(request, "No tiene permisos para gestionar esta organización.")
            return redirect('organization_manage', pk=organization_pk)

    if request.method == 'POST':
        form = VeredaForm(request.POST)
        if form.is_valid():
            vereda = form.save(commit=False)
            vereda.organization_id = organization
            vereda.save()
            messages.success(request, f'Vereda "{vereda.sidewalk_name}" creada correctamente.')
            url = reverse('organization_manage', kwargs={'pk': organization_pk}) + '#veredas'
            return redirect(url)
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = VeredaForm()

    context = {
        'form': form,
        'organization': organization,
        'action': 'create',
        'segment': 'organization'
    }

    return render(request, 'censo/organizacion/vereda_form.html', context)


@login_required
@user_passes_test(is_admin_or_superuser, login_url='home')
def vereda_edit(request, pk):
    """Editar una vereda"""
    vereda = get_object_or_404(Sidewalks, pk=pk)
    organization = vereda.organization_id

    # Verificar permisos
    if not request.user.is_superuser:
        user_profile = getattr(request, 'user_profile', None)
        if not user_profile or user_profile.organization != organization:
            messages.error(request, "No tiene permisos para editar esta vereda.")
            return redirect('organization_manage', pk=organization.pk)

    if request.method == 'POST':
        form = VeredaForm(request.POST, instance=vereda)
        if form.is_valid():
            form.save()
            messages.success(request, f'Vereda "{vereda.sidewalk_name}" actualizada correctamente.')
            url = reverse('organization_manage', kwargs={'pk': organization.pk}) + '#veredas'
            return redirect(url)
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = VeredaForm(instance=vereda)

    context = {
        'form': form,
        'vereda': vereda,
        'organization': organization,
        'action': 'edit',
        'segment': 'organization'
    }

    return render(request, 'censo/organizacion/vereda_form.html', context)


@login_required
@user_passes_test(is_admin_or_superuser, login_url='home')
def vereda_delete(request, pk):
    """Eliminar una vereda"""
    vereda = get_object_or_404(Sidewalks, pk=pk)
    organization = vereda.organization_id

    # Verificar permisos
    if not request.user.is_superuser:
        user_profile = getattr(request, 'user_profile', None)
        if not user_profile or user_profile.organization != organization:
            messages.error(request, "No tiene permisos para eliminar esta vereda.")
            return redirect('organization_manage', pk=organization.pk)

    # Verificar si hay fichas asociadas
    familias_count = vereda.familycard_set.count()

    if request.method == 'POST':
        vereda_nombre = vereda.sidewalk_name

        if familias_count > 0:
            messages.warning(
                request,
                f'La vereda "{vereda_nombre}" tiene {familias_count} familia(s) asociada(s). '
                'Por favor reasigne las familias antes de eliminar la vereda.'
            )
        else:
            vereda.delete()
            messages.success(request, f'Vereda "{vereda_nombre}" eliminada correctamente.')
            url = reverse('organization_manage', kwargs={'pk': organization.pk}) + '#veredas'
            return redirect(url)

    context = {
        'vereda': vereda,
        'organization': organization,
        'familias_count': familias_count,
        'segment': 'organization'
    }

    return render(request, 'censo/organizacion/vereda_confirm_delete.html', context)

