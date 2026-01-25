"""
Script para agregar coordenadas GPS de prueba a veredas
Municipio: Puracé, Cauca, Colombia

Coordenadas base de Puracé: 2.3167° N, 76.4000° W
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import Sidewalks, Organizations
from decimal import Decimal

# Coordenadas de veredas reales de Puracé, Cauca
# Zona montañosa del Parque Nacional Natural Puracé
PURACE_COORDINATES = {
    # Veredas zona norte de Puracé
    'El Cacique': (2.3500, -76.3800),
    'Puracé': (2.3167, -76.4000),
    'San Rafael': (2.3300, -76.3900),
    'Paletará': (2.3400, -76.3700),
    'Poblazón': (2.3600, -76.3950),

    # Veredas zona central
    'Chiribío': (2.3250, -76.4100),
    'Santa Leticia': (2.3350, -76.4050),
    'El Tablazo': (2.3150, -76.3850),
    'La Playa': (2.3450, -76.3800),
    'Coconuco': (2.3550, -76.3900),

    # Veredas zona sur
    'San José': (2.3100, -76.4150),
    'Quintana': (2.3200, -76.4200),
    'Pilimbalá': (2.3050, -76.4050),
    'Kokonuko': (2.3280, -76.3750),
    'Puracé Alto': (2.3380, -76.3650),

    # Veredas adicionales
    'Santa Rosa': (2.3420, -76.3720),
    'El Bosque': (2.3180, -76.3920),
    'La Vuelta': (2.3320, -76.3820),
    'El Salado': (2.3520, -76.3680),
    'Turminá': (2.3580, -76.3780),
}

def main():
    print("=" * 60)
    print("AGREGANDO COORDENADAS GPS A VEREDAS DE PURACÉ, CAUCA")
    print("=" * 60)

    # Obtener todas las organizaciones
    organizations = Organizations.objects.all()
    print(f"\n📊 Organizaciones encontradas: {organizations.count()}")

    for org in organizations:
        print(f"\n🏛️  Organización: {org.organization_name}")

        # Obtener veredas de esta organización
        sidewalks = Sidewalks.objects.filter(organization_id=org)
        print(f"   Veredas: {sidewalks.count()}")

        updated_count = 0

        for sidewalk in sidewalks:
            sidewalk_name = sidewalk.sidewalk_name.strip()

            # Buscar coordenadas exactas o similares
            coords = None

            # Búsqueda exacta
            if sidewalk_name in PURACE_COORDINATES:
                coords = PURACE_COORDINATES[sidewalk_name]
            else:
                # Búsqueda parcial (si el nombre contiene alguna palabra clave)
                for name_key, coordinate in PURACE_COORDINATES.items():
                    if name_key.lower() in sidewalk_name.lower() or \
                       sidewalk_name.lower() in name_key.lower():
                        coords = coordinate
                        break

            if coords:
                lat, lng = coords
                sidewalk.latitude = Decimal(str(lat))
                sidewalk.longitude = Decimal(str(lng))
                sidewalk.save()
                updated_count += 1
                print(f"   ✅ {sidewalk_name}: ({lat}, {lng})")
            else:
                # Asignar coordenada cercana a Puracé con variación aleatoria
                import random
                base_lat = 2.3167 + (random.random() - 0.5) * 0.05  # Variación de ~2.5km
                base_lng = -76.4000 + (random.random() - 0.5) * 0.05

                sidewalk.latitude = Decimal(str(round(base_lat, 4)))
                sidewalk.longitude = Decimal(str(round(base_lng, 4)))
                sidewalk.save()
                updated_count += 1
                print(f"   📍 {sidewalk_name}: ({base_lat:.4f}, {base_lng:.4f}) [generada]")

        print(f"   ✅ Total actualizadas: {updated_count}")

    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)

    total_sidewalks = Sidewalks.objects.all().count()
    with_coords = Sidewalks.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).count()

    print(f"\n📊 Total veredas: {total_sidewalks}")
    print(f"✅ Con coordenadas GPS: {with_coords}")
    print(f"⚠️  Sin coordenadas: {total_sidewalks - with_coords}")
    if total_sidewalks > 0:
        print(f"📈 Porcentaje completado: {(with_coords/total_sidewalks*100):.1f}%")

    # Mostrar por organización
    print("\n📋 Desglose por organización:")
    for org in organizations:
        org_total = Sidewalks.objects.filter(organization_id=org).count()
        org_with_coords = Sidewalks.objects.filter(
            organization_id=org,
            latitude__isnull=False,
            longitude__isnull=False
        ).count()
        print(f"   {org.organization_name}: {org_with_coords}/{org_total}")

    print("\n✅ Coordenadas GPS agregadas exitosamente!")
    print("🗺️  Ahora puedes ver los mapas en:")
    print("   - http://127.0.0.1:8000/mapa/")
    print("   - http://127.0.0.1:8000/mapa/calor/")
    print("   - http://127.0.0.1:8000/mapa/clusters/")
    print("\n🔐 Multi-tenant: Cada organización verá solo sus veredas")
    print("=" * 60)

if __name__ == '__main__':
    main()
