"""
Script de prueba para verificar la creación de fichas familiares
con asignación automática del número de ficha
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import FamilyCard, Sidewalks, Organizations
from censoapp.forms import FormFamilyCard

def test_crear_ficha_familiar():
    """Prueba de creación de ficha familiar con asignación automática de número"""
    print("=" * 80)
    print("PRUEBA: Creación de Ficha Familiar con Asignación Automática")
    print("=" * 80)

    # Obtener datos necesarios
    try:
        sidewalk = Sidewalks.objects.first()
        organization = Organizations.objects.first()

        if not sidewalk or not organization:
            print("❌ ERROR: No hay veredas u organizaciones en la base de datos")
            print("   Por favor, asegúrese de tener datos de prueba")
            return

        print(f"\n✓ Vereda seleccionada: {sidewalk}")
        print(f"✓ Organización seleccionada: {organization}")

    except Exception as e:
        print(f"❌ ERROR al obtener datos: {e}")
        return

    # Verificar el siguiente número de ficha disponible
    next_number = FamilyCard.get_next_family_card_number()
    print(f"\n📋 Siguiente número de ficha disponible: {next_number}")

    # Test 1: Crear ficha usando el formulario (simulando POST)
    print("\n" + "-" * 80)
    print("TEST 1: Crear ficha usando FormFamilyCard")
    print("-" * 80)

    form_data = {
        'address_home': 'Casa de prueba automática',
        'sidewalk_home': sidewalk.id,
        'latitude': '4.5',
        'longitude': '-74.5',
        'zone': 'Rural',
        'organization': organization.id,
    }

    print(f"Datos del formulario: {form_data}")

    form = FormFamilyCard(data=form_data)

    if form.is_valid():
        print("✓ Formulario válido")
        ficha = form.save(commit=False)

        # Asignar número automáticamente (como se hace en la vista)
        ficha.family_card_number = FamilyCard.get_next_family_card_number()
        ficha.state = True

        try:
            ficha.save()
            print(f"✓ Ficha creada exitosamente")
            print(f"  - ID: {ficha.id}")
            print(f"  - Número de ficha: {ficha.family_card_number}")
            print(f"  - Dirección: {ficha.address_home}")
            print(f"  - Vereda: {ficha.sidewalk_home}")
            print(f"  - Organización: {ficha.organization}")

            # Limpiar (eliminar la ficha de prueba)
            ficha.delete()
            print(f"✓ Ficha de prueba eliminada (ID: {ficha.id})")

        except Exception as e:
            print(f"❌ ERROR al guardar la ficha: {e}")
    else:
        print(f"❌ Formulario inválido")
        print(f"   Errores: {form.errors}")
        return

    # Test 2: Crear ficha directamente con el modelo
    print("\n" + "-" * 80)
    print("TEST 2: Crear ficha directamente con el modelo")
    print("-" * 80)

    try:
        ficha2 = FamilyCard(
            address_home='Casa de prueba directa',
            sidewalk_home=sidewalk,
            latitude='4.6',
            longitude='-74.6',
            zone='Urbana',
            organization=organization,
            family_card_number=0,  # Debe asignarse automáticamente
            state=True
        )

        ficha2.save()
        print(f"✓ Ficha creada exitosamente")
        print(f"  - ID: {ficha2.id}")
        print(f"  - Número de ficha: {ficha2.family_card_number}")
        print(f"  - Dirección: {ficha2.address_home}")

        # Verificar que el número se asignó correctamente
        if ficha2.family_card_number > 0:
            print(f"✓ Número de ficha asignado automáticamente: {ficha2.family_card_number}")
        else:
            print(f"❌ ERROR: El número de ficha sigue siendo 0")

        # Limpiar
        ficha2.delete()
        print(f"✓ Ficha de prueba eliminada (ID: {ficha2.id})")

    except Exception as e:
        print(f"❌ ERROR al crear ficha directamente: {e}")

    print("\n" + "=" * 80)
    print("PRUEBA COMPLETADA")
    print("=" * 80)


if __name__ == '__main__':
    test_crear_ficha_familiar()

