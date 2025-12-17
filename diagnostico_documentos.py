"""
Script de diagnóstico para verificar el servidor y las URLs de documentos
"""
import os
import sys

# Verificar si el servidor está corriendo
print("="*70)
print("🔍 DIAGNÓSTICO DEL SISTEMA DE DOCUMENTOS")
print("="*70)
print()

print("✅ PASOS PARA RESOLVER EL PROBLEMA:")
print()
print("1. VERIFICAR QUE EL SERVIDOR ESTÉ CORRIENDO:")
print("   python manage.py runserver")
print()
print("2. ACCEDER A LA URL:")
print("   http://127.0.0.1:8000/documentos/estadisticas/1/")
print()
print("3. ABRIR LA CONSOLA DEL NAVEGADOR (F12) y verificar:")
print("   - Mensajes de error en la pestaña 'Console'")
print("   - Requests en la pestaña 'Network'")
print()
print("4. SI EL PDF NO CARGA EN EL MODAL:")
print("   - Verificar que la URL sea correcta:")
print("     http://127.0.0.1:8000/documento/descargar/1/")
print()
print("   - Probar la URL directamente en el navegador")
print("   - Si funciona directamente, el problema es del iframe")
print()
print("5. SOLUCIÓN ALTERNATIVA:")
print("   - Si el iframe no funciona, usar el botón 'Descargar PDF'")
print("   - O el botón 'Ver Detalles' y luego 'Vista Previa PDF'")
print()
print("="*70)
print("🔧 VERIFICACIONES TÉCNICAS")
print("="*70)
print()

# Verificar archivos
files_to_check = [
    "censoapp/document_views.py",
    "templates/censo/documentos/organization_stats.html",
    "censoapp/urls.py"
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        print(f"✅ {file_path} - Existe")
    else:
        print(f"❌ {file_path} - NO existe")

print()
print("="*70)
print("📋 URLS A VERIFICAR")
print("="*70)
print()
print("Estadísticas de documentos:")
print("  http://127.0.0.1:8000/documentos/estadisticas/")
print()
print("Descargar PDF (reemplazar {id} con ID real):")
print("  http://127.0.0.1:8000/documento/descargar/{id}/")
print()
print("Ver documento:")
print("  http://127.0.0.1:8000/documento/ver/{id}/")
print()
print("="*70)

print()
print("💡 CONSEJO:")
print("Si el modal no funciona, es posible que el navegador esté bloqueando")
print("el iframe por políticas de seguridad. En ese caso:")
print("1. Abre el PDF en una nueva pestaña (botón 'Ver Detalles')")
print("2. O descarga el PDF directamente (botón 'Descargar PDF')")
print()

