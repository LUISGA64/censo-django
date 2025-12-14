# censoapp/middleware.py
"""
Middleware para filtrado automatico por organizacion.
Implementa multi-tenancy a nivel de aplicacion.
"""

import logging

logger = logging.getLogger(__name__)


class OrganizationFilterMiddleware:
    """
    Middleware que inyecta automaticamente la organizacion del usuario
    en el objeto request para todas las vistas.

    Esto permite que las vistas filtren automaticamente los datos
    segun la organizacion del usuario logueado.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Establecer organizacion del usuario en el request
        if request.user.is_authenticated:
            try:
                if hasattr(request.user, 'profile'):
                    request.user_organization = request.user.profile.organization
                    request.can_view_all = request.user.profile.can_view_all_organizations
                    request.user_role = request.user.profile.role
                else:
                    # Usuario sin perfil (puede ser superuser sin perfil)
                    request.user_organization = None
                    request.can_view_all = request.user.is_superuser
                    request.user_role = 'ADMIN' if request.user.is_superuser else None

                    if not request.user.is_superuser:
                        logger.warning(
                            f"Usuario {request.user.username} no tiene perfil asociado. "
                            f"Debe crear un UserProfile desde el admin."
                        )
            except Exception as e:
                logger.error(f"Error al obtener perfil de usuario: {e}")
                request.user_organization = None
                request.can_view_all = False
                request.user_role = None
        else:
            request.user_organization = None
            request.can_view_all = False
            request.user_role = None

        response = self.get_response(request)
        return response


class OrganizationAccessMiddleware:
    """
    Middleware adicional que valida el acceso a organizaciones.
    Registra intentos de acceso a datos de otras organizaciones.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log de accesos para auditoria (solo en produccion)
        if request.user.is_authenticated and hasattr(request, 'user_organization'):
            if request.user_organization:
                logger.debug(
                    f"User: {request.user.username} | "
                    f"Org: {request.user_organization.organization_name} | "
                    f"Path: {request.path}"
                )

        return response

