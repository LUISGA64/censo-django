"""
Script para crear fichas familiares y personas de prueba
Simula el registro completo del sistema de censo
"""

import os
import django
from datetime import date, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from censoapp.models import (
    FamilyCard, Person, Sidewalks, Organizations,
    IdentificationDocumentType, Gender, CivilState,
    EducationLevel, Occupancy, Kinship, SecuritySocial,
    Eps, Handicap
)
from django.contrib.auth.models import User


def obtener_datos_base():
    """Obtener o crear datos base necesarios"""
    print("📋 Verificando datos base...")

    # Verificar tablas relacionadas
    datos = {
        'sidewalks': list(Sidewalks.objects.all()),
        'organizations': list(Organizations.objects.all()),
        'document_types': list(IdentificationDocumentType.objects.all()),
        'genders': list(Gender.objects.all()),
        'civil_states': list(CivilState.objects.all()),
        'education_levels': list(EducationLevel.objects.all()),
        'occupations': list(Occupancy.objects.all()),
        'kinships': list(Kinship.objects.all()),
        'security_socials': list(SecuritySocial.objects.all()),
        'eps': list(Eps.objects.all()),
        'handicaps': list(Handicap.objects.all()),
    }

    # Verificar que existan datos
    for key, value in datos.items():
        if not value:
            print(f"⚠️  ADVERTENCIA: No hay datos en {key}")
        else:
            print(f"✅ {key}: {len(value)} registros")

    return datos


def crear_familias_prueba(num_familias=5):
    """Crear fichas familiares de prueba"""
    print(f"\n🏠 Creando {num_familias} fichas familiares de prueba...")

    datos = obtener_datos_base()

    if not datos['sidewalks'] or not datos['organizations']:
        print("❌ Error: Se necesitan veredas y organizaciones para crear fichas")
        return []

    familias_creadas = []

    # Datos de ejemplo para direcciones
    direcciones = [
        "Casa amarilla al lado de la escuela",
        "Frente al parque principal",
        "Detrás de la iglesia",
        "Al lado del puesto de salud",
        "Cerca del río",
        "Primera casa entrada izquierda",
        "",  # Algunas sin dirección complementaria
        "Casa de dos pisos esquina",
    ]

    zonas = ["Rural", "Urbana"]

    for i in range(num_familias):
        try:
            # Seleccionar datos aleatorios
            sidewalk = random.choice(datos['sidewalks'])
            organization = random.choice(datos['organizations'])
            direccion = random.choice(direcciones)
            zona = random.choice(zonas)

            # Crear ficha familiar
            familia = FamilyCard.objects.create(
                address_home=direccion,
                sidewalk_home=sidewalk,
                zone=zona,
                organization=organization,
                latitude="0",
                longitude="0",
                family_card_number=FamilyCard.get_next_family_card_number(),
                state=True
            )

            familias_creadas.append(familia)
            print(f"✅ Ficha #{familia.family_card_number} - {sidewalk.sidewalk_name} ({zona})")

        except Exception as e:
            print(f"❌ Error al crear ficha {i+1}: {e}")

    return familias_creadas


def generar_fecha_nacimiento(edad_min=18, edad_max=80):
    """Generar fecha de nacimiento aleatoria"""
    hoy = date.today()
    edad = random.randint(edad_min, edad_max)
    dias_extra = random.randint(0, 364)
    fecha = hoy - timedelta(days=(edad * 365 + dias_extra))
    return fecha


def crear_cabeza_familia(familia, datos):
    """Crear el cabeza de familia (mayor de 18 años)"""

    # Datos de ejemplo
    nombres_masculinos = ["Juan", "Carlos", "Pedro", "Luis", "José", "Miguel", "Antonio", "Francisco"]
    nombres_femeninos = ["María", "Ana", "Rosa", "Luz", "Carmen", "Elena", "Sofia", "Laura"]
    apellidos = ["García", "Rodríguez", "López", "Martínez", "González", "Pérez", "Sánchez", "Torres"]

    # Seleccionar género
    genero = random.choice(datos['genders'])

    # Seleccionar nombres según género
    if genero.gender == "Masculino":
        primer_nombre = random.choice(nombres_masculinos)
        segundo_nombre = random.choice(nombres_masculinos) if random.random() > 0.3 else ""
    else:
        primer_nombre = random.choice(nombres_femeninos)
        segundo_nombre = random.choice(nombres_femeninos) if random.random() > 0.3 else ""

    primer_apellido = random.choice(apellidos)
    segundo_apellido = random.choice(apellidos) if random.random() > 0.2 else ""

    # Generar documento
    documento = f"{random.randint(10000000, 99999999)}"

    # Buscar parentesco "Padre" o crear uno genérico
    parentesco_cabeza = None
    for k in datos['kinships']:
        if k.description_kinship.lower() in ['padre', 'cabeza', 'jefe']:
            parentesco_cabeza = k
            break
    if not parentesco_cabeza:
        parentesco_cabeza = datos['kinships'][0]  # Usar el primero si no hay uno apropiado

    try:
        # Generar email válido sin caracteres especiales
        if random.random() > 0.5:
            email = f"{primer_nombre.lower()}{random.randint(1, 999)}@ejemplo.com"
        else:
            email = ""

        persona = Person.objects.create(
            first_name_1=primer_nombre,
            first_name_2=segundo_nombre,
            last_name_1=primer_apellido,
            last_name_2=segundo_apellido,
            identification_person=documento,
            document_type=random.choice([dt for dt in datos['document_types'] if dt.code_document_type == 'CC']),
            date_birth=generar_fecha_nacimiento(18, 65),
            gender=genero,
            civil_state=random.choice(datos['civil_states']),
            education_level=random.choice(datos['education_levels']),
            occupation=random.choice(datos['occupations']),
            kinship=parentesco_cabeza,
            social_insurance=random.choice(datos['security_socials']),
            eps=random.choice(datos['eps']),
            handicap=random.choice(datos['handicaps']),
            cell_phone=f"300{random.randint(1000000, 9999999)}" if random.random() > 0.3 else "",
            personal_email=email,
            family_card=familia,
            family_head=True,
            state=True
        )

        return persona

    except Exception as e:
        print(f"  ❌ Error al crear cabeza de familia: {e}")
        return None


def crear_miembros_familia(familia, cabeza, datos, num_miembros=None):
    """Crear miembros adicionales de la familia"""

    if num_miembros is None:
        num_miembros = random.randint(1, 4)  # 1 a 4 miembros adicionales

    miembros_creados = []

    # Datos de ejemplo
    nombres_masculinos = ["Juan", "Carlos", "Pedro", "Luis", "José", "Miguel", "Antonio", "Diego", "Andrés"]
    nombres_femeninos = ["María", "Ana", "Rosa", "Luz", "Carmen", "Elena", "Sofia", "Laura", "Paula"]

    # Tipos de parentesco
    parentescos_disponibles = {
        'conyuge': ['esposa', 'esposo', 'cónyuge', 'pareja'],
        'hijo': ['hijo', 'hija'],
        'padre': ['padre', 'madre'],
        'hermano': ['hermano', 'hermana'],
    }

    for i in range(num_miembros):
        try:
            # Determinar tipo de miembro
            if i == 0 and cabeza.civil_state.state_civil.lower() == 'casado':
                # Crear cónyuge
                tipo_parentesco = 'conyuge'
                edad_min, edad_max = 18, 65
                genero = Gender.objects.get(gender="Femenino" if cabeza.gender.gender == "Masculino" else "Masculino")
                tipo_documento = [dt for dt in datos['document_types'] if dt.code_document_type == 'CC'][0]
            else:
                # Crear hijo/a
                tipo_parentesco = 'hijo'
                edad_min, edad_max = 0, 25
                genero = random.choice(datos['genders'])

                # Seleccionar tipo de documento según edad
                edad_aprox = random.randint(edad_min, edad_max)
                if edad_aprox < 7:
                    tipo_documento = [dt for dt in datos['document_types'] if dt.code_document_type == 'RC'][0]
                elif edad_aprox < 18:
                    tipo_documento = [dt for dt in datos['document_types'] if dt.code_document_type == 'TI'][0]
                else:
                    tipo_documento = [dt for dt in datos['document_types'] if dt.code_document_type == 'CC'][0]

            # Buscar parentesco apropiado
            parentesco = None
            for k in datos['kinships']:
                for palabra in parentescos_disponibles[tipo_parentesco]:
                    if palabra in k.description_kinship.lower():
                        parentesco = k
                        break
                if parentesco:
                    break

            if not parentesco:
                parentesco = datos['kinships'][1] if len(datos['kinships']) > 1 else datos['kinships'][0]

            # Seleccionar nombres según género
            if genero.gender == "Masculino":
                primer_nombre = random.choice(nombres_masculinos)
                segundo_nombre = random.choice(nombres_masculinos) if random.random() > 0.5 else ""
            else:
                primer_nombre = random.choice(nombres_femeninos)
                segundo_nombre = random.choice(nombres_femeninos) if random.random() > 0.5 else ""

            # Usar apellidos del cabeza de familia
            primer_apellido = cabeza.last_name_1
            segundo_apellido = cabeza.last_name_2 if random.random() > 0.5 else ""

            # Generar documento único
            if tipo_documento.code_document_type == 'RC':
                documento = f"RC{random.randint(1000000, 9999999)}"
            elif tipo_documento.code_document_type == 'TI':
                documento = f"{random.randint(1000000000, 1999999999)}"
            else:
                documento = f"{random.randint(10000000, 99999999)}"

            # Verificar que no exista
            while Person.objects.filter(identification_person=documento).exists():
                documento = f"{int(documento) + 1}"

            persona = Person.objects.create(
                first_name_1=primer_nombre,
                first_name_2=segundo_nombre,
                last_name_1=primer_apellido,
                last_name_2=segundo_apellido,
                identification_person=documento,
                document_type=tipo_documento,
                date_birth=generar_fecha_nacimiento(edad_min, edad_max),
                gender=genero,
                civil_state=random.choice([cs for cs in datos['civil_states'] if cs.state_civil.lower() == 'soltero']) if edad_max < 18 else random.choice(datos['civil_states']),
                education_level=random.choice(datos['education_levels']),
                occupation=random.choice([oc for oc in datos['occupations'] if 'estudiante' in oc.description_occupancy.lower()]) if edad_max < 18 else random.choice(datos['occupations']),
                kinship=parentesco,
                social_insurance=random.choice(datos['security_socials']),
                eps=random.choice(datos['eps']),
                handicap=random.choice(datos['handicaps']),
                cell_phone=f"300{random.randint(1000000, 9999999)}" if random.random() > 0.5 else "",
                personal_email="",
                family_card=familia,
                family_head=False,
                state=True
            )

            miembros_creados.append(persona)

        except Exception as e:
            print(f"  ⚠️  Error al crear miembro {i+1}: {e}")

    return miembros_creados


def main():
    """Función principal"""
    print("=" * 70)
    print("🏠 CREACIÓN DE FICHAS FAMILIARES Y PERSONAS DE PRUEBA")
    print("=" * 70)

    # Verificar datos base
    datos = obtener_datos_base()

    # Verificar que existan datos mínimos
    requeridos = ['sidewalks', 'organizations', 'document_types', 'genders',
                  'civil_states', 'education_levels', 'occupations', 'kinships',
                  'security_socials', 'eps', 'handicaps']

    faltantes = [r for r in requeridos if not datos[r]]

    if faltantes:
        print(f"\n❌ ERROR: Faltan datos en las siguientes tablas: {', '.join(faltantes)}")
        print("Por favor, cargue los datos base primero.")
        return

    # Usar valor por defecto para creación automática
    num_familias = 5
    print(f"\n✅ Se crearán {num_familias} fichas familiares de prueba")

    # Crear familias
    familias = crear_familias_prueba(num_familias)

    if not familias:
        print("\n❌ No se pudieron crear fichas familiares")
        return

    print(f"\n👨‍👩‍👧‍👦 Creando personas para cada familia...")

    total_personas = 0

    for familia in familias:
        print(f"\n📋 Ficha #{familia.family_card_number} - {familia.sidewalk_home.sidewalk_name}")

        # Crear cabeza de familia
        cabeza = crear_cabeza_familia(familia, datos)

        if cabeza:
            print(f"  👤 Cabeza: {cabeza.full_name} - {cabeza.identification_person}")
            total_personas += 1

            # Crear miembros
            miembros = crear_miembros_familia(familia, cabeza, datos)

            for miembro in miembros:
                print(f"    👥 {miembro.full_name} - {miembro.kinship.description_kinship} - {miembro.identification_person}")
                total_personas += 1
        else:
            print("  ❌ No se pudo crear el cabeza de familia")

    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE CREACIÓN")
    print("=" * 70)
    print(f"✅ Fichas familiares creadas: {len(familias)}")
    print(f"✅ Personas creadas: {total_personas}")
    print(f"✅ Promedio de miembros por familia: {total_personas / len(familias):.1f}")
    print("\n🎉 ¡Datos de prueba creados exitosamente!")
    print("=" * 70)


if __name__ == "__main__":
    main()

