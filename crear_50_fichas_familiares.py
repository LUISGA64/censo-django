"""
Script para crear 50 fichas familiares de prueba con entre 3 y 5 integrantes cada una
para la organización 1
"""
import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'censoProject.settings')
django.setup()

from django.db import transaction
from censoapp.models import (
    FamilyCard, Person, Sidewalks, Organizations,
    IdentificationDocumentType, Gender, SecuritySocial, Eps,
    Kinship, Handicap, EducationLevel, CivilState, Occupancy
)

# Nombres y apellidos comunes para generar datos realistas
NOMBRES_MASCULINOS = [
    'Juan', 'Carlos', 'José', 'Luis', 'Miguel', 'Jorge', 'Pedro', 'Andrés',
    'Diego', 'Manuel', 'Roberto', 'Fernando', 'Ricardo', 'Alberto', 'Javier',
    'Antonio', 'Francisco', 'Rafael', 'Sergio', 'Eduardo', 'Daniel', 'Martín',
    'Oscar', 'Gustavo', 'Alejandro', 'Raúl', 'César', 'Pablo', 'Héctor', 'Ramón'
]

NOMBRES_FEMENINOS = [
    'María', 'Ana', 'Carmen', 'Rosa', 'Isabel', 'Laura', 'Patricia', 'Sandra',
    'Claudia', 'Diana', 'Gloria', 'Martha', 'Liliana', 'Andrea', 'Carolina',
    'Beatriz', 'Lucía', 'Elena', 'Teresa', 'Gabriela', 'Mónica', 'Silvia',
    'Adriana', 'Verónica', 'Natalia', 'Paola', 'Valentina', 'Sofía', 'Camila', 'Julia'
]

APELLIDOS = [
    'García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 'Sánchez',
    'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez', 'Díaz', 'Cruz', 'Morales',
    'Hernández', 'Jiménez', 'Ruiz', 'Álvarez', 'Castillo', 'Ortiz', 'Mendoza',
    'Silva', 'Vargas', 'Castro', 'Romero', 'Gutiérrez', 'Vega', 'Medina', 'Ramos'
]

DIRECCIONES = [
    'Vereda alta', 'Vereda baja', 'Sector centro', 'Sector norte',
    'Casa al lado del río', 'Camino principal', 'Sector la loma',
    'Cerca al puente', 'Barrio nuevo', 'Zona escolar'
]

def generar_documento():
    """Genera un número de documento único"""
    return str(random.randint(10000000, 99999999))

def generar_telefono():
    """Genera un número de teléfono"""
    return f'3{random.randint(100000000, 199999999)}'

def generar_fecha_nacimiento(edad_min, edad_max):
    """Genera una fecha de nacimiento basada en un rango de edad"""
    hoy = date.today()
    edad = random.randint(edad_min, edad_max)
    anios_atras = timedelta(days=edad * 365 + random.randint(0, 365))
    return hoy - anios_atras

def normalizar_texto(texto):
    """Elimina acentos y caracteres especiales de un texto"""
    if not texto:
        return ""

    # Reemplazar caracteres acentuados
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N'
    }

    for old, new in replacements.items():
        texto = texto.replace(old, new)

    return texto

def generar_nombre_completo(genero):
    """Genera un nombre completo aleatorio"""
    if genero == 'M':
        primer_nombre = random.choice(NOMBRES_MASCULINOS)
        segundo_nombre = random.choice(NOMBRES_MASCULINOS) if random.random() > 0.5 else ''
    else:
        primer_nombre = random.choice(NOMBRES_FEMENINOS)
        segundo_nombre = random.choice(NOMBRES_FEMENINOS) if random.random() > 0.5 else ''

    primer_apellido = random.choice(APELLIDOS)
    segundo_apellido = random.choice(APELLIDOS)

    return primer_nombre, segundo_nombre, primer_apellido, segundo_apellido

def crear_fichas_familiares():
    """Crea 50 fichas familiares con entre 3 y 5 integrantes cada una"""

    print("=" * 80)
    print("CREACIÓN DE 50 FICHAS FAMILIARES DE PRUEBA")
    print("=" * 80)
    print()

    # Verificar que existan los datos necesarios
    try:
        organization = Organizations.objects.get(id=1)
        print(f"✓ Organización encontrada: {organization}")
    except Organizations.DoesNotExist:
        print("❌ ERROR: No existe la organización con ID 1")
        return

    # Obtener todos los datos necesarios
    try:
        # Obtener todas las veredas disponibles
        sidewalks = list(Sidewalks.objects.all())
        if not sidewalks:
            print("❌ ERROR: No hay veredas en la base de datos")
            return

        document_types = list(IdentificationDocumentType.objects.all())
        genders = {
            'M': Gender.objects.filter(gender__icontains='masculino').first() or Gender.objects.first(),
            'F': Gender.objects.filter(gender__icontains='femenino').first() or Gender.objects.all()[1] if Gender.objects.count() > 1 else Gender.objects.first()
        }
        security_socials = list(SecuritySocial.objects.all())
        eps_list = list(Eps.objects.all())
        kinships = {
            'jefe': Kinship.objects.filter(description_kinship__icontains='jefe').first() or Kinship.objects.first(),
            'esposo': Kinship.objects.filter(description_kinship__icontains='esposo').first() or Kinship.objects.all()[1] if Kinship.objects.count() > 1 else Kinship.objects.first(),
            'hijo': Kinship.objects.filter(description_kinship__icontains='hijo').first() or Kinship.objects.all()[2] if Kinship.objects.count() > 2 else Kinship.objects.first()
        }
        handicaps = list(Handicap.objects.all())
        education_levels = list(EducationLevel.objects.all())
        civil_states = list(CivilState.objects.all())
        occupancies = list(Occupancy.objects.all())

        print(f"✓ {len(sidewalks)} veredas disponibles")
        print(f"✓ {len(document_types)} tipos de documento disponibles")
        print(f"✓ {len(security_socials)} tipos de seguridad social disponibles")
        print(f"✓ {len(eps_list)} EPS disponibles")
        print(f"✓ {len(handicaps)} tipos de capacidades disponibles")
        print(f"✓ {len(education_levels)} niveles educativos disponibles")
        print(f"✓ {len(civil_states)} estados civiles disponibles")
        print(f"✓ {len(occupancies)} ocupaciones disponibles")
        print()

    except Exception as e:
        print(f"❌ ERROR al obtener datos: {e}")
        return

    # Contador de fichas y personas creadas
    fichas_creadas = 0
    personas_creadas = 0
    errores = 0

    # Crear las 50 fichas familiares
    for i in range(1, 51):
        try:
            with transaction.atomic():
                # Determinar el número de integrantes (entre 3 y 5)
                num_integrantes = random.randint(3, 5)

                # Crear la ficha familiar
                sidewalk = random.choice(sidewalks)
                zona = random.choice(['Rural', 'Urbana'])
                direccion = random.choice(DIRECCIONES)

                # Generar coordenadas aleatorias (Colombia aproximadamente)
                latitud = f"{random.uniform(1.0, 12.0):.6f}"
                longitud = f"{random.uniform(-79.0, -66.0):.6f}"

                ficha = FamilyCard.objects.create(
                    address_home=f"{direccion} #{random.randint(1, 100)}",
                    sidewalk_home=sidewalk,
                    latitude=latitud,
                    longitude=longitud,
                    zone=zona,
                    organization=organization,
                    state=True
                )

                fichas_creadas += 1

                # Crear el cabeza de familia (adulto de 25-60 años)
                genero_jefe = random.choice(['M', 'F'])
                nombre1, nombre2, apellido1, apellido2 = generar_nombre_completo(genero_jefe)

                documento_jefe = generar_documento()
                while Person.objects.filter(identification_person=documento_jefe).exists():
                    documento_jefe = generar_documento()

                jefe = Person.objects.create(
                    first_name_1=nombre1,
                    first_name_2=nombre2,
                    last_name_1=apellido1,
                    last_name_2=apellido2,
                    identification_person=documento_jefe,
                    document_type=random.choice(document_types),
                    cell_phone=generar_telefono(),
                    personal_email=f"{normalizar_texto(nombre1).lower()}.{normalizar_texto(apellido1).lower()}@example.com" if random.random() > 0.3 else None,
                    gender=genders[genero_jefe],
                    date_birth=generar_fecha_nacimiento(25, 60),
                    social_insurance=random.choice(security_socials),
                    eps=random.choice(eps_list),
                    kinship=kinships['jefe'],
                    handicap=random.choice(handicaps),
                    education_level=random.choice(education_levels),
                    civil_state=random.choice(civil_states),
                    occupation=random.choice(occupancies),
                    family_card=ficha,
                    family_head=True,
                    state=True
                )
                personas_creadas += 1

                # Crear cónyuge si hay al menos 4 integrantes (adulto de 23-55 años)
                if num_integrantes >= 4:
                    genero_conyuge = 'F' if genero_jefe == 'M' else 'M'
                    nombre1, nombre2, apellido1_c, apellido2_c = generar_nombre_completo(genero_conyuge)

                    documento_conyuge = generar_documento()
                    while Person.objects.filter(identification_person=documento_conyuge).exists():
                        documento_conyuge = generar_documento()

                    conyuge = Person.objects.create(
                        first_name_1=nombre1,
                        first_name_2=nombre2,
                        last_name_1=apellido1_c,
                        last_name_2=apellido2_c,
                        identification_person=documento_conyuge,
                        document_type=random.choice(document_types),
                        cell_phone=generar_telefono() if random.random() > 0.5 else None,
                        personal_email=None,
                        gender=genders[genero_conyuge],
                        date_birth=generar_fecha_nacimiento(23, 55),
                        social_insurance=random.choice(security_socials),
                        eps=random.choice(eps_list),
                        kinship=kinships['esposo'],
                        handicap=random.choice(handicaps),
                        education_level=random.choice(education_levels),
                        civil_state=random.choice(civil_states),
                        occupation=random.choice(occupancies),
                        family_card=ficha,
                        family_head=False,
                        state=True
                    )
                    personas_creadas += 1
                    num_integrantes -= 1

                # Crear hijos (el resto de integrantes, entre 0-17 años)
                for j in range(num_integrantes - 1):
                    genero_hijo = random.choice(['M', 'F'])
                    nombre1, nombre2, _, _ = generar_nombre_completo(genero_hijo)

                    documento_hijo = generar_documento()
                    while Person.objects.filter(identification_person=documento_hijo).exists():
                        documento_hijo = generar_documento()

                    hijo = Person.objects.create(
                        first_name_1=nombre1,
                        first_name_2=nombre2,
                        last_name_1=apellido1,  # Heredan el apellido del jefe
                        last_name_2=apellido2,
                        identification_person=documento_hijo,
                        document_type=random.choice(document_types),
                        cell_phone=None,
                        personal_email=None,
                        gender=genders[genero_hijo],
                        date_birth=generar_fecha_nacimiento(0, 17),
                        social_insurance=random.choice(security_socials),
                        eps=random.choice(eps_list),
                        kinship=kinships['hijo'],
                        handicap=random.choice(handicaps),
                        education_level=random.choice(education_levels),
                        civil_state=civil_states[0] if len(civil_states) > 0 else random.choice(civil_states),
                        occupation=occupancies[0] if len(occupancies) > 0 else random.choice(occupancies),
                        family_card=ficha,
                        family_head=False,
                        state=True
                    )
                    personas_creadas += 1

                # Mostrar progreso
                if i % 10 == 0:
                    print(f"✓ Progreso: {i}/50 fichas creadas ({personas_creadas} personas)")

        except Exception as e:
            errores += 1
            print(f"❌ Error al crear ficha {i}: {e}")
            continue

    # Resumen final
    print()
    print("=" * 80)
    print("RESUMEN DE CREACIÓN")
    print("=" * 80)
    print(f"✓ Fichas familiares creadas: {fichas_creadas}/50")
    print(f"✓ Personas creadas: {personas_creadas}")
    print(f"✓ Promedio de integrantes por familia: {personas_creadas/fichas_creadas:.2f}" if fichas_creadas > 0 else "N/A")

    if errores > 0:
        print(f"⚠️  Errores encontrados: {errores}")

    # Verificación final
    print()
    print("=" * 80)
    print("VERIFICACIÓN FINAL")
    print("=" * 80)

    fichas_org1 = FamilyCard.objects.filter(organization_id=1, state=True).count()
    personas_org1 = Person.objects.filter(family_card__organization_id=1, state=True).count()
    jefes_familia = Person.objects.filter(family_card__organization_id=1, family_head=True, state=True).count()

    print(f"📊 Total de fichas en organización 1: {fichas_org1}")
    print(f"📊 Total de personas en organización 1: {personas_org1}")
    print(f"📊 Total de jefes de familia: {jefes_familia}")

    # Mostrar algunas fichas creadas
    print()
    print("=" * 80)
    print("MUESTRA DE FICHAS CREADAS (últimas 5)")
    print("=" * 80)

    ultimas_fichas = FamilyCard.objects.filter(organization_id=1).order_by('-id')[:5]
    for ficha in ultimas_fichas:
        miembros = Person.objects.filter(family_card=ficha, state=True)
        jefe = miembros.filter(family_head=True).first()
        print(f"\nFicha #{ficha.family_card_number}:")
        print(f"  📍 Ubicación: {ficha.address_home} - {ficha.sidewalk_home}")
        print(f"  👥 Integrantes: {miembros.count()}")
        if jefe:
            print(f"  👤 Jefe de familia: {jefe.first_name_1} {jefe.last_name_1}")

    print()
    print("=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)


if __name__ == '__main__':
    crear_fichas_familiares()

