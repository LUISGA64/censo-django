"""
Script para activar la funcionalidad de Datos de Vivienda
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import SystemParameters

print("=" * 70)
print("ACTIVACIÓN DE DATOS DE VIVIENDA")
print("=" * 70)

# Crear o actualizar el parámetro
param, created = SystemParameters.objects.get_or_create(
    key='Datos de Vivienda',
    defaults={'value': 'S'}
)

if created:
    print(f"\n✅ Parámetro creado: {param.key} = {param.value}")
else:
    print(f"\n📋 Parámetro existente: {param.key} = {param.value}")
    
    if param.value != 'S':
        param.value = 'S'
        param.save()
        print(f"✅ Parámetro actualizado a: {param.value}")
    else:
        print(f"ℹ️  El parámetro ya estaba activado")

print("\n" + "=" * 70)
print("✅ DATOS DE VIVIENDA ACTIVADOS")
print("=" * 70)
print("\nAhora la funcionalidad de 'Datos de Vivienda' está habilitada.")
print("Puedes editar fichas familiares y registrar:")
print("  - Materiales de construcción (techo, pared, piso)")
print("  - Estado de los materiales")
print("  - Datos de ocupación (familias, habitaciones, personas)")
print("  - Propiedad y cocina")
print("  - Condiciones adicionales (humo, ventilación, iluminación)")
print("\n" + "=" * 70)

