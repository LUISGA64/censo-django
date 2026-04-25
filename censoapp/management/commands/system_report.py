"""
Comando para generar un reporte del estado actual del sistema.
Muestra estadísticas de usuarios, organizaciones, fichas y personas.

Uso:
    python manage.py system_report
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import models
from censoapp.models import (
    UserProfile, Organizations, FamilyCard, Person,
    Sidewalks, Association
)
from datetime import datetime


class Command(BaseCommand):
    help = 'Genera un reporte del estado actual del sistema'

    def handle(self, *args, **options):
        self.stdout.write('\n' + '='*70)
        self.stdout.write(
            self.style.SUCCESS('    REPORTE DE ESTADO DEL SISTEMA - CENSO DJANGO')
        )
        self.stdout.write('='*70 + '\n')

        # Fecha y hora
        self.stdout.write(f'Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')

        # 1. ASOCIACIONES
        self.stdout.write(self.style.HTTP_INFO('📋 ASOCIACIONES:'))
        associations = Association.objects.all()
        self.stdout.write(f'   Total: {associations.count()}')
        for assoc in associations:
            self.stdout.write(f'   - {assoc.association_name}')

        # 2. ORGANIZACIONES
        self.stdout.write('\n' + self.style.HTTP_INFO('🏢 ORGANIZACIONES:'))
        organizations = Organizations.objects.all()
        self.stdout.write(f'   Total: {organizations.count()}')
        for org in organizations:
            sidewalks = Sidewalks.objects.filter(organization_id=org).count()
            families = FamilyCard.objects.filter(organization=org, state=True).count()
            persons = Person.objects.filter(
                family_card__organization=org,
                state=True
            ).count()
            self.stdout.write(
                f'   - {org.organization_name}'
                f'\n     Veredas: {sidewalks} | Fichas: {families} | Personas: {persons}'
            )

        # 3. USUARIOS
        self.stdout.write('\n' + self.style.HTTP_INFO('👥 USUARIOS Y PERMISOS:'))
        users = User.objects.all()
        profiles = UserProfile.objects.all()
        self.stdout.write(f'   Total usuarios: {users.count()}')
        self.stdout.write(f'   Con perfil: {profiles.count()}')

        # Desglose por rol
        roles = profiles.values_list('role', flat=True).distinct()
        for role in roles:
            count = profiles.filter(role=role).count()
            self.stdout.write(f'   - {role}: {count} usuario(s)')

        # Listar usuarios
        self.stdout.write('\n   Detalle de usuarios:')
        for user in User.objects.all():
            if hasattr(user, 'profile'):
                profile = user.profile
                access = '🔓 Global' if profile.can_view_all_organizations else '🔒 Local'
                status = '✅' if profile.is_active else '❌'
                self.stdout.write(
                    f'   {status} {user.username} - {profile.organization.organization_name} '
                    f'({profile.role}) {access}'
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'   ⚠️  {user.username} - SIN PERFIL')
                )

        # 4. DATOS CENSALES
        self.stdout.write('\n' + self.style.HTTP_INFO('📊 DATOS CENSALES:'))

        total_families = FamilyCard.objects.filter(state=True).count()
        total_persons = Person.objects.filter(state=True).count()

        self.stdout.write(f'   Fichas familiares: {total_families}')
        self.stdout.write(f'   Personas registradas: {total_persons}')

        if total_families > 0:
            avg_members = total_persons / total_families
            self.stdout.write(f'   Promedio miembros/familia: {avg_members:.2f}')

        # Distribución por género
        from django.db.models import Count
        gender_dist = Person.objects.filter(state=True).values(
            'gender__gender'
        ).annotate(count=Count('id'))

        if gender_dist:
            self.stdout.write('\n   Distribución por género:')
            for g in gender_dist:
                gender = g['gender__gender'] or 'Sin especificar'
                count = g['count']
                percentage = (count / total_persons * 100) if total_persons > 0 else 0
                self.stdout.write(f'   - {gender}: {count} ({percentage:.1f}%)')

        # 5. VEREDAS
        self.stdout.write('\n' + self.style.HTTP_INFO('🗺️  VEREDAS:'))
        sidewalks = Sidewalks.objects.all()
        self.stdout.write(f'   Total: {sidewalks.count()}')

        sidewalk_stats = Sidewalks.objects.annotate(
            num_families=Count('familycard', filter=models.Q(familycard__state=True))
        ).order_by('-num_families')[:5]

        if sidewalk_stats:
            self.stdout.write('\n   Top 5 veredas con más fichas:')
            for sw in sidewalk_stats:
                self.stdout.write(f'   - {sw.sidewalk_name}: {sw.num_families} fichas')

        # 6. SEGURIDAD Y AUDITORÍA
        self.stdout.write('\n' + self.style.HTTP_INFO('🔐 SEGURIDAD:'))

        # Verificar si hay historial configurado
        try:
            from simple_history.models import HistoricalRecords
            self.stdout.write('   ✅ Auditoría: django-simple-history instalado')

            # Contar registros históricos
            from censoapp.models import HistoricalFamilyCard, HistoricalPerson
            hist_families = HistoricalFamilyCard.objects.count()
            hist_persons = HistoricalPerson.objects.count()
            self.stdout.write(f'   - Registros históricos fichas: {hist_families}')
            self.stdout.write(f'   - Registros históricos personas: {hist_persons}')
        except:
            self.stdout.write('   ⚠️  Auditoría: No configurada')

        # Multi-organización
        if organizations.count() > 1:
            self.stdout.write('   ✅ Multi-organización: ACTIVA')
        else:
            self.stdout.write('   ⚠️  Multi-organización: Solo 1 organización')

        # Cache
        from django.core.cache import cache
        try:
            cache.set('test_key', 'test_value', 10)
            if cache.get('test_key') == 'test_value':
                self.stdout.write('   ✅ Cache: Funcionando')
            else:
                self.stdout.write('   ⚠️  Cache: No disponible')
        except:
            self.stdout.write('   ⚠️  Cache: Error al verificar')

        # 7. RESUMEN
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('✅ REPORTE COMPLETADO'))
        self.stdout.write('='*70 + '\n')

