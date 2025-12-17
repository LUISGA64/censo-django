"""
Script de depuración para probar la vista de estadísticas de documentos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import Organizations, GeneratedDocument
from django.contrib.auth.models import User

def debug_stats():
    print("\n" + "="*70)
    print("🔍 DEPURACIÓN DE ESTADÍSTICAS DE DOCUMENTOS")
    print("="*70 + "\n")

    # Verificar organizaciones
    print("📋 Organizaciones en el sistema:")
    orgs = Organizations.objects.all()
    if orgs.exists():
        for org in orgs:
            print(f"   - {org.organization_name} (ID: {org.id})")
            docs_count = GeneratedDocument.objects.filter(organization=org).count()
            print(f"     Documentos: {docs_count}")
    else:
        print("   ⚠️  No hay organizaciones registradas")

    print()

    # Verificar documentos
    print("📄 Documentos en el sistema:")
    total_docs = GeneratedDocument.objects.all().count()
    print(f"   Total: {total_docs}")

    if total_docs > 0:
        for doc in GeneratedDocument.objects.all()[:5]:
            print(f"   - {doc.document_number} | {doc.document_type.document_type_name} | {doc.status}")

    print()

    # Verificar usuario actual
    print("👤 Usuarios del sistema:")
    users = User.objects.all()
    for user in users:
        print(f"   - {user.username} (Admin: {user.is_superuser})")
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
            if profile.organization:
                print(f"     Organización: {profile.organization.organization_name}")
            else:
                print(f"     ⚠️  Sin organización asignada")
        else:
            print(f"     ⚠️  Sin perfil de usuario")

    print()

    # URLs para acceder
    print("🌐 URLs para probar:")
    print("   Admin - Vista general:")
    print("   http://127.0.0.1:8000/documentos/estadisticas/")
    print()
    if orgs.exists():
        for org in orgs:
            print(f"   {org.organization_name}:")
            print(f"   http://127.0.0.1:8000/documentos/estadisticas/{org.id}/")

    print("\n" + "="*70)
    print("✅ DEPURACIÓN COMPLETADA")
    print("="*70 + "\n")

if __name__ == '__main__':
    debug_stats()

