"""
Script para limpiar todos los datos de fichas familiares, personas y documentos generados.
Esto es útil para hacer pruebas limpias de la carga masiva.
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import Person, FamilyCard, GeneratedDocument
from django.db import transaction


def limpiar_datos():
    """
    Elimina todos los datos de:
    - Documentos generados
    - Personas
    - Fichas familiares
    """

    print("=" * 60)
    print("LIMPIEZA DE DATOS PARA PRUEBA DE CARGA MASIVA")
    print("=" * 60)
    print()

    # Contar registros antes de eliminar
    count_documentos = GeneratedDocument.objects.count()
    count_personas = Person.objects.count()
    count_fichas = FamilyCard.objects.count()

    print(f"📊 Registros actuales:")
    print(f"   - Documentos generados: {count_documentos}")
    print(f"   - Personas: {count_personas}")
    print(f"   - Fichas familiares: {count_fichas}")
    print()

    if count_documentos == 0 and count_personas == 0 and count_fichas == 0:
        print("✅ No hay datos para eliminar. La base de datos ya está limpia.")
        return

    # Confirmar eliminación
    respuesta = input("⚠️  ¿Estás seguro de que deseas eliminar TODOS estos datos? (si/no): ")

    if respuesta.lower() not in ['si', 'sí', 's', 'yes', 'y']:
        print("❌ Operación cancelada.")
        return

    print()
    print("🗑️  Iniciando eliminación de datos...")
    print()

    try:
        with transaction.atomic():
            # 1. Eliminar documentos generados
            if count_documentos > 0:
                print(f"   Eliminando {count_documentos} documentos generados...", end=" ")
                GeneratedDocument.objects.all().delete()
                print("✅")

            # 2. Eliminar personas
            if count_personas > 0:
                print(f"   Eliminando {count_personas} personas...", end=" ")
                Person.objects.all().delete()
                print("✅")

            # 3. Eliminar fichas familiares
            if count_fichas > 0:
                print(f"   Eliminando {count_fichas} fichas familiares...", end=" ")
                FamilyCard.objects.all().delete()
                print("✅")

        print()
        print("=" * 60)
        print("✅ DATOS ELIMINADOS EXITOSAMENTE")
        print("=" * 60)
        print()
        print("📊 Registros actuales:")
        print(f"   - Documentos generados: {GeneratedDocument.objects.count()}")
        print(f"   - Personas: {Person.objects.count()}")
        print(f"   - Fichas familiares: {FamilyCard.objects.count()}")
        print()
        print("🎉 La base de datos está lista para la prueba de carga masiva.")

    except Exception as e:
        print()
        print(f"❌ Error durante la eliminación: {str(e)}")
        print("   Los cambios han sido revertidos.")
        return


if __name__ == '__main__':
    limpiar_datos()

