"""
Script para verificar documentos generados y mostrar cómo acceder a ellos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import GeneratedDocument, Person

print("=" * 70)
print("📄 DOCUMENTOS GENERADOS EN EL SISTEMA")
print("=" * 70)

docs = GeneratedDocument.objects.all().order_by('-created_at')
print(f"\nTotal de documentos: {docs.count()}")

if docs.exists():
    print("\n" + "=" * 70)
    print("LISTA DE DOCUMENTOS:")
    print("=" * 70)

    for doc in docs:
        print(f"\n📋 Documento #{doc.id}")
        print(f"   Tipo: {doc.document_type.document_type_name}")
        print(f"   Número: {doc.document_number}")
        print(f"   Persona: {doc.person.full_name}")
        print(f"   Identificación: {doc.person.identification_person}")
        print(f"   Organización: {doc.organization.organization_name}")
        print(f"   Estado: {doc.get_status_display()}")
        print(f"   Fecha expedición: {doc.issue_date}")
        if doc.expiration_date:
            print(f"   Fecha vencimiento: {doc.expiration_date}")
        print(f"   📍 URL para ver: http://127.0.0.1:8000/documento/ver/{doc.id}/")
        print("-" * 70)
else:
    print("\n⚠️  No hay documentos generados aún.")
    print("\n📝 Para generar un documento:")
    print("   1. Accede al detalle de una persona")
    print("   2. Click en 'Generar Documento'")
    print("   3. Selecciona el tipo de documento")
    print("   4. Click en 'Generar Documento'")

print("\n" + "=" * 70)
print("🔍 CÓMO VISUALIZAR UN DOCUMENTO")
print("=" * 70)

print("\n📌 OPCIÓN 1: Desde el detalle de persona")
print("   1. Ir a: http://127.0.0.1:8000/personas/detail/<ID_PERSONA>/")
print("   2. Ver sección 'Documentos Generados' (si existe)")
print("   3. Click en el documento deseado")

print("\n📌 OPCIÓN 2: URL Directa")
print("   http://127.0.0.1:8000/documento/ver/<ID_DOCUMENTO>/")

print("\n📌 OPCIÓN 3: Ver todos los documentos de una persona")
print("   http://127.0.0.1:8000/documento/persona/<ID_PERSONA>/")

print("\n" + "=" * 70)
print("🧪 GENERAR DOCUMENTO DE PRUEBA")
print("=" * 70)

# Buscar una persona para generar documento de prueba
personas = Person.objects.filter(state=True, family_head=True)[:5]

if personas.exists():
    print("\n✅ Personas disponibles para generar documentos:\n")
    for p in personas:
        print(f"   👤 {p.full_name}")
        print(f"      ID: {p.id}")
        print(f"      Identificación: {p.identification_person}")
        print(f"      🔗 Generar documento: http://127.0.0.1:8000/documento/generar/{p.id}/")
        print()
else:
    print("\n⚠️  No hay personas registradas.")

print("=" * 70)

