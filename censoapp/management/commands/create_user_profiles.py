"""
Comando de management para crear perfiles de usuario para usuarios existentes.
Útil durante la migración a multi-organización.

Uso:
    python manage.py create_user_profiles
    python manage.py create_user_profiles --organization=1  # Para una organización específica
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from censoapp.models import UserProfile, Organizations


class Command(BaseCommand):
    help = 'Crea perfiles de usuario para usuarios existentes sin perfil'

    def add_arguments(self, parser):
        parser.add_argument(
            '--organization',
            type=int,
            help='ID de la organización para asignar a todos los usuarios',
        )
        parser.add_argument(
            '--role',
            type=str,
            default='OPERATOR',
            choices=['ADMIN', 'OPERATOR', 'VIEWER'],
            help='Rol por defecto para los usuarios (default: OPERATOR)',
        )

    def handle(self, *args, **options):
        organization_id = options.get('organization')
        role = options.get('role', 'OPERATOR')

        # Obtener usuarios sin perfil
        users_without_profile = User.objects.filter(profile__isnull=True)
        total_users = users_without_profile.count()

        if total_users == 0:
            self.stdout.write(
                self.style.SUCCESS('✓ Todos los usuarios ya tienen perfil asignado.')
            )
            return

        self.stdout.write(
            self.style.WARNING(f'Encontrados {total_users} usuarios sin perfil.')
        )

        # Determinar organización a asignar
        if organization_id:
            try:
                organization = Organizations.objects.get(pk=organization_id)
                self.stdout.write(
                    self.style.SUCCESS(f'Usando organización: {organization.organization_name}')
                )
            except Organizations.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Organización con ID {organization_id} no existe.')
                )
                return
        else:
            # Usar la primera organización disponible
            organization = Organizations.objects.first()
            if not organization:
                self.stdout.write(
                    self.style.ERROR('❌ No hay organizaciones en la base de datos. Cree una primero.')
                )
                return

            self.stdout.write(
                self.style.WARNING(
                    f'No se especificó organización. Usando: {organization.organization_name}'
                )
            )

        # Crear perfiles
        created_count = 0
        skipped_count = 0

        for user in users_without_profile:
            try:
                # Determinar permisos especiales para superusuarios
                can_view_all = user.is_superuser
                user_role = 'ADMIN' if user.is_superuser else role

                profile = UserProfile.objects.create(
                    user=user,
                    organization=organization,
                    role=user_role,
                    can_view_all_organizations=can_view_all,
                    is_active=True
                )

                created_count += 1

                status = '🔑 Admin Global' if can_view_all else f'👤 {user_role}'
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ {user.username} - {status} - {organization.organization_name}'
                    )
                )

            except Exception as e:
                skipped_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Error con {user.username}: {str(e)}')
                )

        # Resumen
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS(f'✓ Perfiles creados: {created_count}'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'⚠ Usuarios omitidos: {skipped_count}'))
        self.stdout.write('='*70 + '\n')

        # Listar organizaciones disponibles para referencia
        if created_count > 0:
            self.stdout.write('\nOrganizaciones disponibles:')
            for org in Organizations.objects.all():
                user_count = UserProfile.objects.filter(organization=org).count()
                self.stdout.write(f'  - {org.organization_name} (ID: {org.id}) - {user_count} usuarios')

