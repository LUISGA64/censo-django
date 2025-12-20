"""
Script para verificar que el usuario actual tenga perfil y organización.
Ayuda a diagnosticar el error: "Organizations matching query does not exist."
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.contrib.auth.models import User
from censoapp.models import Organizations, UserProfile

def verificar_usuarios():
    print("=" * 70)
    print("VERIFICACIÓN DE USUARIOS, PERFILES Y ORGANIZACIONES")
    print("=" * 70)
    print()

    usuarios = User.objects.all()

    if not usuarios.exists():
        print("❌ No hay usuarios en el sistema")
        return

    print(f"Total de usuarios: {usuarios.count()}")
    print()

    problemas = []

    for user in usuarios:
        print(f"Usuario: {user.username}")
        print(f"  • Email: {user.email}")
        print(f"  • Superusuario: {'Sí' if user.is_superuser else 'No'}")
        print(f"  • Activo: {'Sí' if user.is_active else 'No'}")

        # Verificar perfil
        if hasattr(user, 'userprofile'):
            print(f"  • Perfil: ✅ Existe")
            profile = user.userprofile

            # Verificar organización
            if profile.organization:
                print(f"  • Organización: ✅ {profile.organization.organization_name}")
            else:
                print(f"  • Organización: ❌ NO TIENE ORGANIZACIÓN")
                if not user.is_superuser:
                    problemas.append({
                        'usuario': user.username,
                        'problema': 'No tiene organización asociada'
                    })
        else:
            print(f"  • Perfil: ❌ NO TIENE PERFIL")
            if not user.is_superuser:
                problemas.append({
                    'usuario': user.username,
                    'problema': 'No tiene perfil de usuario'
                })

        print()

    # Resumen de problemas
    if problemas:
        print("=" * 70)
        print("⚠️  PROBLEMAS ENCONTRADOS")
        print("=" * 70)
        print()

        for i, problema in enumerate(problemas, 1):
            print(f"{i}. Usuario: {problema['usuario']}")
            print(f"   Problema: {problema['problema']}")
            print()

        print("=" * 70)
        print("🔧 SOLUCIONES SUGERIDAS")
        print("=" * 70)
        print()

        for problema in problemas:
            usuario = User.objects.get(username=problema['usuario'])
            print(f"Para el usuario '{problema['usuario']}':")

            if problema['problema'] == 'No tiene perfil de usuario':
                print("  Crear perfil con:")
                print(f"    from censoapp.models import UserProfile")
                print(f"    user = User.objects.get(username='{problema['usuario']}')")
                print(f"    org = Organizations.objects.first()  # o seleccionar una específica")
                print(f"    UserProfile.objects.create(user=user, organization=org)")
                print()

            elif problema['problema'] == 'No tiene organización asociada':
                print("  Asignar organización con:")
                print(f"    from censoapp.models import Organizations, UserProfile")
                print(f"    user = User.objects.get(username='{problema['usuario']}')")
                print(f"    org = Organizations.objects.first()  # o seleccionar una específica")
                print(f"    user.userprofile.organization = org")
                print(f"    user.userprofile.save()")
                print()
    else:
        print("=" * 70)
        print("✅ TODOS LOS USUARIOS TIENEN PERFIL Y ORGANIZACIÓN")
        print("=" * 70)

    # Mostrar organizaciones disponibles
    print()
    print("=" * 70)
    print("ORGANIZACIONES DISPONIBLES")
    print("=" * 70)
    print()

    orgs = Organizations.objects.all()
    if orgs.exists():
        for org in orgs:
            print(f"• ID: {org.id} - {org.organization_name}")
            usuarios_org = UserProfile.objects.filter(organization=org).count()
            print(f"  Usuarios asociados: {usuarios_org}")
            print()
    else:
        print("❌ No hay organizaciones en el sistema")
        print()
        print("Crear una organización con:")
        print("  from censoapp.models import Organizations")
        print("  org = Organizations.objects.create(")
        print("      organization_name='Mi Organización',")
        print("      organization_identification='123456789',")
        print("      organization_type_document='NIT',")
        print("      organization_address='Dirección',")
        print("      organization_municipality='Municipio',")
        print("      organization_departament='Departamento'")
        print("  )")


def corregir_usuario_actual():
    """Función para corregir el usuario actual si tiene problemas"""
    print()
    print("=" * 70)
    print("🔧 CORRECCIÓN AUTOMÁTICA")
    print("=" * 70)
    print()

    # Obtener el último usuario activo que no sea superuser
    try:
        user = User.objects.filter(is_superuser=False, is_active=True).first()

        if not user:
            print("ℹ️  No hay usuarios regulares activos para corregir")
            return

        print(f"Verificando usuario: {user.username}")

        # Verificar si tiene perfil
        if not hasattr(user, 'userprofile'):
            print("  ❌ Usuario sin perfil")

            # Obtener o crear una organización
            org = Organizations.objects.first()
            if not org:
                print("  ⚠️  No hay organizaciones, creando una de prueba...")
                org = Organizations.objects.create(
                    organization_name='Organización de Prueba',
                    organization_identification='123456789',
                    organization_type_document='NIT',
                    organization_address='Calle Principal',
                    organization_municipality='Municipio',
                    organization_departament='Departamento'
                )
                print(f"  ✅ Organización creada: {org.organization_name}")

            # Crear perfil
            profile = UserProfile.objects.create(
                user=user,
                organization=org
            )
            print(f"  ✅ Perfil creado y asociado a: {org.organization_name}")

        elif not user.userprofile.organization:
            print("  ❌ Usuario sin organización")

            # Obtener o crear una organización
            org = Organizations.objects.first()
            if not org:
                print("  ⚠️  No hay organizaciones, creando una de prueba...")
                org = Organizations.objects.create(
                    organization_name='Organización de Prueba',
                    organization_identification='123456789',
                    organization_type_document='NIT',
                    organization_address='Calle Principal',
                    organization_municipality='Municipio',
                    organization_departament='Departamento'
                )
                print(f"  ✅ Organización creada: {org.organization_name}")

            user.userprofile.organization = org
            user.userprofile.save()
            print(f"  ✅ Organización asignada: {org.organization_name}")

        else:
            print(f"  ✅ Usuario tiene perfil y organización: {user.userprofile.organization.organization_name}")

    except Exception as e:
        print(f"  ❌ Error durante la corrección: {str(e)}")


if __name__ == '__main__':
    verificar_usuarios()

    # Preguntar si se desea corregir automáticamente
    print()
    print("=" * 70)
    respuesta = input("¿Desea intentar corregir automáticamente los problemas? (s/n): ").strip().lower()

    if respuesta == 's':
        corregir_usuario_actual()
        print()
        print("Verificando nuevamente...")
        print()
        verificar_usuarios()

    print()
    print("=" * 70)
    print("✅ Verificación completa")
    print("=" * 70)

