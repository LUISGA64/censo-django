"""
Utilidades para importación masiva de datos desde Excel.
Permite importar fichas familiares y personas de forma masiva.
"""
from datetime import datetime
from django.db import transaction
from django.core.exceptions import ValidationError
from openpyxl import load_workbook
import re


class ImportadorMasivo:
    """
    Clase para manejar la importación masiva de datos desde Excel.
    """

    def __init__(self, archivo_excel, organization):
        self.archivo = archivo_excel
        self.organization = organization
        self.errores = []
        self.advertencias = []
        self.fichas_creadas = 0
        self.personas_creadas = 0

    def validar_estructura(self):
        """Valida que el archivo tenga la estructura correcta."""
        try:
            wb = load_workbook(self.archivo, data_only=True)

            # Verificar que existan las hojas necesarias
            if 'Fichas' not in wb.sheetnames:
                self.errores.append("Falta la hoja 'Fichas' en el archivo Excel")
                return False

            if 'Personas' not in wb.sheetnames:
                self.errores.append("Falta la hoja 'Personas' en el archivo Excel")
                return False

            # Validar columnas de Fichas
            ws_fichas = wb['Fichas']
            columnas_fichas_requeridas = [
                'numero_ficha', 'vereda', 'zona', 'direccion',
                'tipo_vivienda', 'material_paredes', 'material_piso', 'material_techo'
            ]

            headers_fichas = [cell.value for cell in ws_fichas[1]]
            for col in columnas_fichas_requeridas:
                if col not in headers_fichas:
                    self.errores.append(f"Falta la columna '{col}' en la hoja Fichas")

            # Validar columnas de Personas
            ws_personas = wb['Personas']
            columnas_personas_requeridas = [
                'numero_ficha', 'primer_nombre', 'primer_apellido',
                'identificacion', 'tipo_documento', 'fecha_nacimiento',
                'genero', 'parentesco', 'cabeza_familia'
            ]

            headers_personas = [cell.value for cell in ws_personas[1]]
            for col in columnas_personas_requeridas:
                if col not in headers_personas:
                    self.errores.append(f"Falta la columna '{col}' en la hoja Personas")

            return len(self.errores) == 0

        except Exception as e:
            self.errores.append(f"Error al leer el archivo Excel: {str(e)}")
            return False

    def extraer_datos_fichas(self):
        """Extrae los datos de fichas del Excel."""
        wb = load_workbook(self.archivo, data_only=True)
        ws = wb['Fichas']

        # Obtener headers
        headers = [cell.value for cell in ws[1]]

        # Extraer datos
        fichas = []
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row):  # Saltar filas vacías
                continue

            ficha_data = {}
            for idx, header in enumerate(headers):
                ficha_data[header] = row[idx]

            ficha_data['fila_excel'] = row_idx
            fichas.append(ficha_data)

        return fichas

    def extraer_datos_personas(self):
        """Extrae los datos de personas del Excel."""
        wb = load_workbook(self.archivo, data_only=True)
        ws = wb['Personas']

        # Obtener headers
        headers = [cell.value for cell in ws[1]]

        # Extraer datos
        personas = []
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row):  # Saltar filas vacías
                continue

            persona_data = {}
            for idx, header in enumerate(headers):
                persona_data[header] = row[idx]

            persona_data['fila_excel'] = row_idx
            personas.append(persona_data)

        return personas

    def validar_datos_ficha(self, ficha_data, fila):
        """Valida los datos de una ficha."""
        errores_fila = []

        # Validar número de ficha
        if not ficha_data.get('numero_ficha'):
            errores_fila.append(f"Fila {fila}: Número de ficha es obligatorio")

        # Validar vereda
        if not ficha_data.get('vereda'):
            errores_fila.append(f"Fila {fila}: Vereda es obligatoria")

        # Validar zona
        if ficha_data.get('zona') and ficha_data['zona'] not in ['U', 'R', 'URBANA', 'RURAL']:
            errores_fila.append(f"Fila {fila}: Zona debe ser 'U' (Urbana) o 'R' (Rural)")

        return errores_fila

    def validar_datos_persona(self, persona_data, fila):
        """Valida los datos de una persona."""
        errores_fila = []

        # Validar número de ficha
        if not persona_data.get('numero_ficha'):
            errores_fila.append(f"Fila {fila}: Número de ficha es obligatorio")

        # Validar nombres
        if not persona_data.get('primer_nombre'):
            errores_fila.append(f"Fila {fila}: Primer nombre es obligatorio")

        if not persona_data.get('primer_apellido'):
            errores_fila.append(f"Fila {fila}: Primer apellido es obligatorio")

        # Validar identificación
        if not persona_data.get('identificacion'):
            errores_fila.append(f"Fila {fila}: Identificación es obligatoria")
        else:
            # Verificar que sea alfanumérica
            if not re.match(r'^[A-Za-z0-9]+$', str(persona_data['identificacion'])):
                errores_fila.append(f"Fila {fila}: Identificación debe ser alfanumérica")

        # Validar fecha de nacimiento
        if not persona_data.get('fecha_nacimiento'):
            errores_fila.append(f"Fila {fila}: Fecha de nacimiento es obligatoria")
        else:
            try:
                if isinstance(persona_data['fecha_nacimiento'], str):
                    datetime.strptime(persona_data['fecha_nacimiento'], '%Y-%m-%d')
            except ValueError:
                errores_fila.append(f"Fila {fila}: Fecha de nacimiento inválida (formato: YYYY-MM-DD)")

        # Validar género
        if not persona_data.get('genero'):
            errores_fila.append(f"Fila {fila}: Género es obligatorio")

        # Validar cabeza de familia
        cabeza = str(persona_data.get('cabeza_familia', '')).upper()
        if cabeza not in ['SI', 'NO', 'SÍ', 'S', 'N', '1', '0', 'TRUE', 'FALSE']:
            errores_fila.append(f"Fila {fila}: Cabeza de familia debe ser SI/NO")

        return errores_fila

    def validar_duplicados(self, personas_data):
        """Valida que no haya identificaciones duplicadas."""
        from censoapp.models import Person

        identificaciones = [p.get('identificacion') for p in personas_data if p.get('identificacion')]

        # Duplicados en el Excel
        duplicados_excel = set([x for x in identificaciones if identificaciones.count(x) > 1])
        if duplicados_excel:
            for dup in duplicados_excel:
                self.errores.append(f"Identificación duplicada en Excel: {dup}")

        # Duplicados en la base de datos
        for persona_data in personas_data:
            identificacion = persona_data.get('identificacion')
            if identificacion:
                if Person.objects.filter(identification_person=identificacion).exists():
                    fila = persona_data.get('fila_excel', '?')
                    self.errores.append(f"Fila {fila}: Identificación {identificacion} ya existe en la base de datos")

    def validar_todo(self):
        """Ejecuta todas las validaciones."""
        # Validar estructura
        if not self.validar_estructura():
            return False

        # Extraer datos
        fichas_data = self.extraer_datos_fichas()
        personas_data = self.extraer_datos_personas()

        # Validar cada ficha
        for ficha in fichas_data:
            errores = self.validar_datos_ficha(ficha, ficha.get('fila_excel', '?'))
            self.errores.extend(errores)

        # Validar cada persona
        for persona in personas_data:
            errores = self.validar_datos_persona(persona, persona.get('fila_excel', '?'))
            self.errores.extend(errores)

        # Validar duplicados
        self.validar_duplicados(personas_data)

        # Validar que cada ficha tenga al menos una persona
        fichas_numeros = set([f.get('numero_ficha') for f in fichas_data])
        personas_fichas = set([p.get('numero_ficha') for p in personas_data])

        fichas_sin_personas = fichas_numeros - personas_fichas
        if fichas_sin_personas:
            for num_ficha in fichas_sin_personas:
                self.advertencias.append(f"Ficha {num_ficha} no tiene personas asociadas")

        return len(self.errores) == 0

    def importar(self):
        """
        Ejecuta la importación de datos.
        Retorna un diccionario con el resultado.
        """
        from censoapp.models import FamilyCard, Person, Sidewalks, Gender, Kinship
        from censoapp.models import IdentificationDocumentType, EducationLevel
        from censoapp.models import CivilState, Occupancy, SecuritySocial, Eps, Handicap

        if not self.validar_todo():
            return {
                'exito': False,
                'errores': self.errores,
                'advertencias': self.advertencias
            }

        try:
            with transaction.atomic():
                # Extraer datos
                fichas_data = self.extraer_datos_fichas()
                personas_data = self.extraer_datos_personas()

                # Diccionario para mapear número de ficha a objeto FamilyCard
                fichas_creadas_map = {}

                # Crear fichas familiares
                for ficha_data in fichas_data:
                    # Obtener o crear vereda
                    vereda_nombre = ficha_data.get('vereda', 'Sin Vereda')
                    vereda, _ = Sidewalks.objects.get_or_create(
                        sidewalk_name=vereda_nombre,
                        defaults={'state': True}
                    )

                    # Normalizar zona
                    zona = ficha_data.get('zona', 'R')
                    if zona in ['URBANA', 'U']:
                        zona = 'U'
                    else:
                        zona = 'R'

                    # Crear ficha familiar
                    ficha = FamilyCard.objects.create(
                        family_card_number=ficha_data.get('numero_ficha'),
                        sidewalk_home=vereda,
                        zone=zona,
                        address=ficha_data.get('direccion', ''),
                        type_housing=ficha_data.get('tipo_vivienda', 'Propia'),
                        organization=self.organization,
                        state=True
                    )

                    fichas_creadas_map[ficha_data.get('numero_ficha')] = ficha
                    self.fichas_creadas += 1

                # Crear personas
                for persona_data in personas_data:
                    # Obtener la ficha
                    numero_ficha = persona_data.get('numero_ficha')
                    ficha = fichas_creadas_map.get(numero_ficha)

                    if not ficha:
                        continue

                    # Obtener o crear género
                    genero_nombre = persona_data.get('genero', 'Masculino')
                    genero, _ = Gender.objects.get_or_create(
                        gender=genero_nombre,
                        defaults={'state': True}
                    )

                    # Obtener o crear tipo de documento
                    tipo_doc_nombre = persona_data.get('tipo_documento', 'CC')
                    tipo_doc, _ = IdentificationDocumentType.objects.get_or_create(
                        identification_document_type=tipo_doc_nombre,
                        defaults={'state': True}
                    )

                    # Obtener o crear parentesco
                    parentesco_nombre = persona_data.get('parentesco', 'Otro')
                    parentesco, _ = Kinship.objects.get_or_create(
                        kinship=parentesco_nombre,
                        defaults={'state': True}
                    )

                    # Obtener defaults para campos obligatorios
                    edu_level = EducationLevel.objects.first()
                    civil_state = CivilState.objects.first()
                    occupation = Occupancy.objects.first()
                    security_social = SecuritySocial.objects.first()
                    eps = Eps.objects.first()
                    handicap = Handicap.objects.first()

                    # Normalizar cabeza de familia
                    cabeza_str = str(persona_data.get('cabeza_familia', 'NO')).upper()
                    es_cabeza = cabeza_str in ['SI', 'SÍ', 'S', '1', 'TRUE']

                    # Parsear fecha de nacimiento
                    fecha_nac = persona_data.get('fecha_nacimiento')
                    if isinstance(fecha_nac, str):
                        fecha_nac = datetime.strptime(fecha_nac, '%Y-%m-%d').date()

                    # Crear persona
                    Person.objects.create(
                        first_name_1=persona_data.get('primer_nombre', ''),
                        first_name_2=persona_data.get('segundo_nombre', ''),
                        last_name_1=persona_data.get('primer_apellido', ''),
                        last_name_2=persona_data.get('segundo_apellido', ''),
                        identification_person=str(persona_data.get('identificacion', '')),
                        document_type=tipo_doc,
                        date_birth=fecha_nac,
                        gender=genero,
                        kinship=parentesco,
                        family_head=es_cabeza,
                        family_card=ficha,
                        education_level=edu_level,
                        civil_state=civil_state,
                        occupation=occupation,
                        social_insurance=security_social,
                        eps=eps,
                        handicap=handicap,
                        state=True
                    )

                    self.personas_creadas += 1

                return {
                    'exito': True,
                    'fichas_creadas': self.fichas_creadas,
                    'personas_creadas': self.personas_creadas,
                    'advertencias': self.advertencias
                }

        except Exception as e:
            return {
                'exito': False,
                'errores': [f"Error durante la importación: {str(e)}"],
                'advertencias': self.advertencias
            }

