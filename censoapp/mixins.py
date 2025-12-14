# censoapp/mixins.py
"""
Mixins para implementar filtrado automatico por organizacion en vistas.
Estos mixins permiten multi-tenancy a nivel de aplicacion.
"""

from django.core.exceptions import PermissionDenied
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


class OrganizationFilterMixin:
    """
    Mixin que filtra automaticamente los querysets por organizacion del usuario.

    Uso:
        class MiVista(OrganizationFilterMixin, ListView):
            model = FamilyCard
            # El queryset se filtra automaticamente

    Comportamiento:
        - Superusuarios: Ven todos los datos
        - Usuarios con can_view_all_organizations: Ven todos los datos
        - Usuarios normales: Solo ven datos de su organizacion
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        # Superusuarios y usuarios con permiso global ven todo
        if self.request.user.is_superuser or getattr(self.request, 'can_view_all', False):
            logger.debug(f"Usuario {self.request.user.username} tiene acceso global")
            return queryset

        # Usuarios normales solo ven su organizacion
        user_organization = getattr(self.request, 'user_organization', None)

        if not user_organization:
            logger.warning(
                f"Usuario {self.request.user.username} no tiene organizacion asignada. "
                f"Retornando queryset vacio."
            )
            return queryset.none()

        # Filtrar segun el modelo
        model = queryset.model

        # FamilyCard tiene organization directamente
        if hasattr(model, 'organization'):
            filtered_qs = queryset.filter(organization=user_organization)
            logger.debug(
                f"Filtrando {model.__name__} por organization={user_organization.organization_name}"
            )
            return filtered_qs

        # Person se filtra a traves de family_card
        elif hasattr(model, 'family_card'):
            filtered_qs = queryset.filter(
                family_card__organization=user_organization
            )
            logger.debug(
                f"Filtrando {model.__name__} por family_card__organization={user_organization.organization_name}"
            )
            return filtered_qs

        # Sidewalks tiene organization_id
        elif hasattr(model, 'organization_id'):
            filtered_qs = queryset.filter(organization_id=user_organization)
            logger.debug(
                f"Filtrando {model.__name__} por organization_id={user_organization.organization_name}"
            )
            return filtered_qs

        # MaterialConstructionFamilyCard se filtra a traves de family_card
        elif model.__name__ == 'MaterialConstructionFamilyCard':
            filtered_qs = queryset.filter(
                family_card__organization=user_organization
            )
            logger.debug(
                f"Filtrando MaterialConstructionFamilyCard por family_card__organization={user_organization.organization_name}"
            )
            return filtered_qs

        # Para otros modelos, retornar queryset completo con warning
        logger.warning(
            f"Modelo {model.__name__} no tiene relacion con organization. "
            f"Retornando queryset completo. Considere agregar filtrado manual."
        )
        return queryset


class OrganizationPermissionMixin:
    """
    Mixin que valida que el usuario tenga permiso para acceder al objeto.
    Se usa en vistas de detalle, edicion y eliminacion.

    Uso:
        class UpdateFamily(OrganizationPermissionMixin, UpdateView):
            model = FamilyCard
            # Valida que el usuario pueda editar esta ficha
    """

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Superusuarios y usuarios con acceso global siempre pueden
        if self.request.user.is_superuser or getattr(self.request, 'can_view_all', False):
            return obj

        # Validar que el objeto pertenezca a la organizacion del usuario
        user_organization = getattr(self.request, 'user_organization', None)

        if not user_organization:
            logger.error(
                f"Usuario {self.request.user.username} sin organizacion intento acceder a {obj}"
            )
            raise PermissionDenied("Usuario sin organizacion asignada")

        # Validar segun el modelo
        obj_organization = None

        if hasattr(obj, 'organization'):
            obj_organization = obj.organization
        elif hasattr(obj, 'family_card') and hasattr(obj.family_card, 'organization'):
            obj_organization = obj.family_card.organization
        elif hasattr(obj, 'organization_id'):
            obj_organization = obj.organization_id

        if obj_organization and obj_organization != user_organization:
            logger.error(
                f"Usuario {self.request.user.username} de org {user_organization.organization_name} "
                f"intento acceder a objeto de org {obj_organization.organization_name}"
            )
            raise PermissionDenied("No tiene permiso para acceder a este recurso")

        return obj


class OrganizationFormMixin:
    """
    Mixin para formularios que limita las opciones de organizacion
    segun el usuario logueado.

    Uso:
        class CreateFamilyView(OrganizationFormMixin, CreateView):
            model = FamilyCard
            # Los campos de organizacion/vereda se limitan automaticamente
    """

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Si el usuario no tiene acceso global, limitar opciones
        if not (self.request.user.is_superuser or getattr(self.request, 'can_view_all', False)):
            user_organization = getattr(self.request, 'user_organization', None)

            if user_organization:
                # Limitar organizacion si existe en el formulario
                if 'organization' in form.fields:
                    form.fields['organization'].queryset = form.fields['organization'].queryset.filter(
                        id=user_organization.id
                    )
                    form.fields['organization'].initial = user_organization
                    form.fields['organization'].widget.attrs['readonly'] = True

                # Limitar veredas a las de su organizacion
                if 'sidewalk_home' in form.fields:
                    from .models import Sidewalks
                    form.fields['sidewalk_home'].queryset = Sidewalks.objects.filter(
                        organization_id=user_organization
                    )

        return form

