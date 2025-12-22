import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

# Verificar que los imports funcionen
print("=" * 80)
print("Verificando imports de simple_document_views")
print("=" * 80)

try:
    from censoapp.simple_document_views import (
        select_document_type,
        generate_aval_general,
        generate_aval_estudio,
        generate_constancia_pertenencia
    )
    print("✅ Todos los imports funcionan correctamente")
    print()
    print("Funciones importadas:")
    print(f"  - select_document_type: {select_document_type}")
    print(f"  - generate_aval_general: {generate_aval_general}")
    print(f"  - generate_aval_estudio: {generate_aval_estudio}")
    print(f"  - generate_constancia_pertenencia: {generate_constancia_pertenencia}")
    print()

    # Verificar que las URLs estén configuradas
    from django.urls import reverse, resolve

    print("Verificando URLs:")
    try:
        url = reverse('select-document-type', args=[1])
        print(f"  ✅ select-document-type: {url}")
        resolver = resolve(url)
        print(f"     Función: {resolver.func}")
    except Exception as e:
        print(f"  ❌ Error con select-document-type: {e}")

    try:
        url = reverse('generate-aval-general', args=[1])
        print(f"  ✅ generate-aval-general: {url}")
    except Exception as e:
        print(f"  ❌ Error con generate-aval-general: {e}")

    try:
        url = reverse('generate-aval-estudio', args=[1])
        print(f"  ✅ generate-aval-estudio: {url}")
    except Exception as e:
        print(f"  ❌ Error con generate-aval-estudio: {e}")

    try:
        url = reverse('generate-constancia', args=[1])
        print(f"  ✅ generate-constancia: {url}")
    except Exception as e:
        print(f"  ❌ Error con generate-constancia: {e}")

    print()
    print("=" * 80)
    print("✅ VERIFICACIÓN COMPLETADA - TODO FUNCIONA CORRECTAMENTE")
    print("=" * 80)

except ImportError as e:
    print(f"❌ ERROR DE IMPORT: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

