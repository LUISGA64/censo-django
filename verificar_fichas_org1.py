"""
Script para verificar las fichas familiares creadas en la organización 1
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import FamilyCard, Person, Organizations
from django.db.models import Count

def verificar_fichas():
    """Verifica y muestra estadísticas de las fichas creadas"""

    print("=" * 80)
    print("VERIFICACIÓN DE FICHAS FAMILIARES - ORGANIZACIÓN 1")
    print("=" * 80)
    print()

    try:
        org = Organizations.objects.get(id=1)
        print(f"📋 Organización: {org}")
        print()
    except Organizations.DoesNotExist:
        print("❌ No existe la organización con ID 1")
        return

    # Estadísticas generales
    fichas = FamilyCard.objects.filter(organization_id=1, state=True)
    total_fichas = fichas.count()
    personas = Person.objects.filter(family_card__organization_id=1, state=True)
    total_personas = personas.count()
    jefes = personas.filter(family_head=True).count()

    print("📊 ESTADÍSTICAS GENERALES")
    print("-" * 80)
    print(f"Total de fichas familiares: {total_fichas}")
    print(f"Total de personas: {total_personas}")
    print(f"Jefes de familia: {jefes}")
    print(f"Promedio de integrantes por familia: {total_personas/total_fichas:.2f}")
    print()

    # Distribución por número de integrantes
    print("📊 DISTRIBUCIÓN POR NÚMERO DE INTEGRANTES")
    print("-" * 80)

    # Contar manualmente los integrantes de cada ficha
    distribucion_dict = {}
    for ficha in fichas:
        num_integrantes = Person.objects.filter(family_card=ficha, state=True).count()
        if num_integrantes in distribucion_dict:
            distribucion_dict[num_integrantes] += 1
        else:
            distribucion_dict[num_integrantes] = 1

    # Ordenar y mostrar
    for num in sorted(distribucion_dict.keys()):
        cant = distribucion_dict[num]
        porcentaje = (cant / total_fichas) * 100
        barra = "█" * int(porcentaje / 2)
        print(f"{num} integrantes: {cant:3d} fichas ({porcentaje:5.1f}%) {barra}")

    print()

    # Distribución por zona
    print("📊 DISTRIBUCIÓN POR ZONA")
    print("-" * 80)

    zonas = fichas.values('zone').annotate(
        cantidad=Count('id')
    ).order_by('-cantidad')

    for zona in zonas:
        nombre = zona['zone']
        cant = zona['cantidad']
        porcentaje = (cant / total_fichas) * 100
        print(f"{nombre:10s}: {cant:3d} fichas ({porcentaje:5.1f}%)")

    print()

    # Distribución por vereda
    print("📊 DISTRIBUCIÓN POR VEREDA")
    print("-" * 80)

    veredas = fichas.values('sidewalk_home__sidewalk_name').annotate(
        cantidad=Count('id')
    ).order_by('-cantidad')

    for vereda in veredas:
        nombre = vereda['sidewalk_home__sidewalk_name']
        cant = vereda['cantidad']
        porcentaje = (cant / total_fichas) * 100
        print(f"{nombre:20s}: {cant:3d} fichas ({porcentaje:5.1f}%)")

    print()

    # Estadísticas de personas
    print("📊 ESTADÍSTICAS DE PERSONAS")
    print("-" * 80)

    # Por género
    generos = personas.values('gender__gender').annotate(
        cantidad=Count('id')
    ).order_by('-cantidad')

    print("Por género:")
    for genero in generos:
        nombre = genero['gender__gender']
        cant = genero['cantidad']
        porcentaje = (cant / total_personas) * 100
        print(f"  {nombre:15s}: {cant:3d} personas ({porcentaje:5.1f}%)")

    print()

    # Por parentesco
    parentescos = personas.values('kinship__description_kinship').annotate(
        cantidad=Count('id')
    ).order_by('-cantidad')

    print("Por parentesco:")
    for parentesco in parentescos:
        nombre = parentesco['kinship__description_kinship']
        cant = parentesco['cantidad']
        porcentaje = (cant / total_personas) * 100
        print(f"  {nombre:15s}: {cant:3d} personas ({porcentaje:5.1f}%)")

    print()

    # Últimas 10 fichas creadas
    print("📋 ÚLTIMAS 10 FICHAS CREADAS")
    print("-" * 80)

    ultimas = FamilyCard.objects.filter(organization_id=1).order_by('-id')[:10]

    for ficha in ultimas:
        miembros = Person.objects.filter(family_card=ficha, state=True)
        jefe = miembros.filter(family_head=True).first()

        print(f"\nFicha #{ficha.family_card_number}:")
        print(f"  📍 Ubicación: {ficha.address_home}")
        print(f"  🏘️  Vereda: {ficha.sidewalk_home}")
        print(f"  🌍 Zona: {ficha.zone}")
        print(f"  👥 Integrantes: {miembros.count()}")

        if jefe:
            print(f"  👤 Jefe de familia: {jefe.first_name_1} {jefe.first_name_2 or ''} {jefe.last_name_1} {jefe.last_name_2 or ''}")
            print(f"     📱 Tel: {jefe.cell_phone or 'N/A'}")
            print(f"     📧 Email: {jefe.personal_email or 'N/A'}")

        print(f"  👨‍👩‍👧‍👦 Miembros:")
        for persona in miembros:
            tipo = "👤 JEFE" if persona.family_head else f"   {persona.kinship.description_kinship}"
            print(f"     - {tipo}: {persona.first_name_1} {persona.last_name_1} (Doc: {persona.identification_person})")

    print()
    print("=" * 80)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 80)


if __name__ == '__main__':
    verificar_fichas()

