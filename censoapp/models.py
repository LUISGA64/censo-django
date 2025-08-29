from django.core.exceptions import ValidationError
from django.db import models
from .choices import zone
from django.db.models import Max


class Association(models.Model):
    association_name = models.CharField(max_length=50, null=False, blank=False)
    association_identification = models.CharField(max_length=15, null=False, blank=False)
    association_type_document = models.CharField(max_length=3, null=False, blank=False, default='NIT',
                                                 help_text="Ingrese NIT")
    association_phone_mobile = models.CharField(max_length=15, help_text="Ingrese número de celular")
    association_phone = models.CharField(max_length=15)
    association_address = models.CharField(null=False, blank=False, max_length=50)
    association_departament = models.CharField(null=False, blank=False, max_length=15,
                                               help_text="Registre el departamento")
    association_email = models.EmailField(blank=False, null=False)
    association_logo = models.ImageField('Logo Association', null=True, blank=False, upload_to="Association")

    def __str__(self):
        return f"{self.association_name} {self.association_identification}"


class Organizations(models.Model):
    organization_name = models.CharField(max_length=50, null=False, blank=False)
    organization_identification = models.CharField(max_length=15, blank=False, null=False, unique=True)
    organization_type_identification = models.CharField(max_length=3, default='NIT')
    organization_territory = models.CharField(max_length=50, blank=False, null=False)
    organization_email = models.EmailField(null=False, blank=False)
    organization_mobile_phone = models.CharField(max_length=15)
    organization_phone = models.CharField(max_length=15)
    organization_address = models.CharField(max_length=50, null=False, blank=False)
    organization_logo = models.ImageField('Logo Organization', blank=False, null=False, upload_to="Images")
    association_id = models.ForeignKey('Association', on_delete=models.CASCADE)

    def __str__(self):
        return self.organization_name


class Sidewalks(models.Model):
    sidewalk_name = models.CharField(blank=False, null=False, max_length=40)
    organization_id = models.ForeignKey('Organizations', blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.sidewalk_name


class CivilState(models.Model):
    code_state_civil = models.CharField(blank=False, null=False, max_length=1)
    state_civil = models.CharField(blank=False, unique=True, null=False, max_length=25)

    def __str__(self):
        return f"{self.state_civil}"


class EducationLevel(models.Model):
    code_education_level = models.CharField(blank=False, null=False, max_length=1)
    education_level = models.CharField(blank=False, null=False, unique=True, max_length=50)

    def __str__(self):
        return self.education_level


class Eps(models.Model):
    code_eps = models.CharField(blank=False, null=False, unique=True, max_length=6)
    name_eps = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"{self.name_eps}"


class Kinship(models.Model):
    code_kinship = models.CharField(blank=False, null=False, max_length=1)
    description_kinship = models.CharField(max_length=25, blank=False, null=False)

    def __str__(self):
        return self.description_kinship


class Occupancy(models.Model):
    description_occupancy = models.CharField(blank=False, null=False, max_length=35)

    def __str__(self):
        return self.description_occupancy


class DocumentType(models.Model):
    code_document_type = models.CharField(blank=False, null=False, unique=True, max_length=3)
    document_type = models.CharField(blank=False, null=False, max_length=25)

    def __str__(self):
        return f"{self.document_type}"


class Gender(models.Model):
    gender_code = models.CharField(blank=False, null=False, max_length=1)
    gender = models.CharField(blank=False, null=False, max_length=15)

    def __str__(self):
        return f"{self.gender}"


class Handicap(models.Model):
    code_handicap = models.CharField(blank=False, null=False, max_length=1)
    handicap = models.CharField(blank=False, null=False, max_length=50)

    def __str__(self):
        return f"{self.handicap}"


class SecuritySocial(models.Model):
    code_security_social = models.CharField(blank=False, null=False, unique=True, max_length=5)
    affiliation = models.CharField(blank=False, null=False, max_length=30)

    def __str__(self):
        return f"{self.affiliation}"


class FamilyCard(models.Model):
    address_home = models.CharField(blank=True, null=True, max_length=50, help_text="Registre Información Adicional",
                                    verbose_name="Dirección Vivienda")
    sidewalk_home = models.ForeignKey('Sidewalks', null=False, blank=False, on_delete=models.CASCADE,
                                      verbose_name="Vereda",
                                      help_text="Seleccione la vereda donde vive")
    latitude = models.CharField(default='0', max_length=15, help_text="Registre la latitud", verbose_name="Latitud")
    longitude = models.CharField(default='0', max_length=15, help_text="Registre la longitud", verbose_name="Longitud")
    zone = models.CharField(choices=zone, blank=False, null=False, max_length=10, help_text="Seleccione Urbana o Rural",
                            verbose_name="Zona")
    organization = models.ForeignKey('Organizations', on_delete=models.CASCADE, default='',
                                     verbose_name="Resguardo", help_text="Seleccione el Resguardo",
                                     null=False, blank=False)
    family_card_number = models.IntegerField(blank=False, null=False, unique=True, verbose_name="Número de Familia",
                                             default=0)
    state = models.BooleanField(blank=False, null=False, default=True, verbose_name="Estado de la Ficha",
                                help_text="¿La ficha familiar está activa?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Última Actualización")

    class Meta:
        ordering = ['family_card_number']

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        self.address_home = self.address_home.strip().lower().capitalize() if self.address_home else ''
        super().save(*args, **kwargs)

    @classmethod
    def get_next_family_card_number(cls):
        max_num = cls.objects.aggregate(Max('family_card_number'))['family_card_number__max'] or 0
        return max_num + 1

    @classmethod
    def get_count_members(cls, family_card_id):
        return Person.objects.filter(family_card_id=family_card_id, state=True).count()


class Person(models.Model):
    first_name_1 = models.CharField(blank=False, null=False, max_length=30, verbose_name="Primer Nombre")
    first_name_2 = models.CharField(blank=True, null=True, max_length=30, verbose_name="Segundo Nombre")
    last_name_1 = models.CharField(blank=False, null=False, max_length=30, verbose_name="Primer Apellido")
    last_name_2 = models.CharField(blank=True, null=True, max_length=30, verbose_name="Segundo Apellido")
    identification_person = models.CharField(blank=False, null=False, unique=True, max_length=15,
                                             verbose_name="Identificación")
    document_type = models.ForeignKey('DocumentType', on_delete=models.CASCADE, verbose_name="Tipo de documento",
                                      blank=False, null=False)

    cell_phone = models.CharField(blank=True, null=True, max_length=15, verbose_name="Teléfono Móvil")

    personal_email = models.EmailField(blank=True, null=True, max_length=50, verbose_name="Correo Personal")

    gender = models.ForeignKey('Gender', on_delete=models.CASCADE, verbose_name="Género")

    date_birth = models.DateField(blank=False, null=False, verbose_name="Fecha de Nacimiento")

    social_insurance = models.ForeignKey('SecuritySocial', on_delete=models.CASCADE,
                                         verbose_name="Seguridad Social", max_length=50)

    eps = models.ForeignKey('Eps', on_delete=models.CASCADE, verbose_name="EPS")

    kinship = models.ForeignKey('Kinship', blank=False, null=False, on_delete=models.CASCADE,
                                verbose_name="Parentescos")
    handicap = models.ForeignKey(Handicap, max_length=50, on_delete=models.CASCADE, verbose_name="Capacidades Diversas")

    education_level = models.ForeignKey('EducationLevel', on_delete=models.CASCADE, verbose_name="Nivel Educativo")

    civil_state = models.ForeignKey('CivilState', on_delete=models.CASCADE, verbose_name="Estado Civil")

    occupation = models.ForeignKey('Occupancy', blank=False, null=False, on_delete=models.CASCADE,
                                   verbose_name="Ocupación")

    family_card = models.ForeignKey('FamilyCard', on_delete=models.CASCADE, verbose_name="Ficha Familiar")

    family_head = models.BooleanField(blank=False, null=False, default=False, verbose_name="Cabeza de Familia")
    state = models.BooleanField(blank=False, null=False, default=True, verbose_name="Vivo")

    def __str__(self):
        return (f"{self.first_name_1} {self.first_name_2} {self.last_name_1} {self.last_name_2} - "
                f"{self.identification_person}")

    def clean(self):
        super().clean()
        if self.family_head:
            qs = Person.objects.filter(family_card=self.family_card, family_head=True)

            if self.pk:
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError("Ya existe una persona registrada como cabeza de familia en esta ficha.")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.first_name_1 = self.first_name_1.strip().lower().capitalize()
        self.first_name_2 = self.first_name_2.strip().lower().capitalize()
        self.last_name_1 = self.last_name_1.strip().lower().capitalize()
        self.last_name_2 = self.last_name_2.strip().lower().capitalize()
        self.personal_email = self.personal_email.strip().lower() if self.personal_email else ''
        self.cell_phone = self.cell_phone.strip() if self.cell_phone else ''
        self.identification_person = self.identification_person.strip()
        # super(Person, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name_1} {self.first_name_2} {self.last_name_1} {self.last_name_2}"

    @property
    def calcular_anios(self):
        from datetime import date
        today = date.today()
        years = today.year - self.date_birth.year
        months = today.month - self.date_birth.month
        days = today.day - self.date_birth.day

        if days < 0:
            months -= 1
        if months < 0:
            years -= 1
            months += 12

        if years > 0:
            return f"{years} años"
        else:
            return f"{months} meses"


class SystemParameters(models.Model):
    key = models.CharField(blank=False, null=False, unique=True, max_length=100)
    value = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.key}: {self.value}"


class Charge(models.Model):
    charge_name = models.CharField(max_length=150, blank=False, null=False, unique=True)
    authorized_sign = models.BooleanField(default=False,
                                          help_text="¿Esta persona está autorizada para firmar documentos?")

    def __str__(self):
        return f"{self.charge_name} - {'Autorizado' if self.authorized_sign else 'No Autorizado'}"

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"


class MaterialConstruction(models.Model):
    material_name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    roof = models.BooleanField(default=False, help_text="¿El material es utilizado en techos?")
    wall = models.BooleanField(default=False, help_text="¿El material es utilizado en paredes?")
    floor = models.BooleanField(default=False, help_text="¿El material es utilizado en pisos?")

    def __str__(self):
        return f"{self.material_name}"

    class Meta:
        verbose_name = "Material de Construcción"
        verbose_name_plural = "Materiales de Construcción"
        ordering = ['material_name']

    def clean(self):
        if not (self.roof or self.wall or self.floor):
            raise ValidationError("Debe seleccionar al menos un tipo de uso para el material (techo, pared o piso).")
        super().clean()

    def save(self, *args, **kwargs):
        self.material_name = self.material_name.strip().lower().capitalize()
        super().save(*args, **kwargs)


class HomeOwnership(models.Model):
    ownership_type = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.ownership_type

    class Meta:
        verbose_name = "Tipo de Propiedad"
        verbose_name_plural = "Tipos de Propiedad"


class CookingFuel(models.Model):
    fuel_type = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.fuel_type

    class Meta:
        verbose_name = "Tipo de Combustible"
        verbose_name_plural = "Tipos de Combustible"


class WaterSource(models.Model):
    source_type = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.source_type

    class Meta:
        verbose_name = "Fuente de Agua"
        verbose_name_plural = "Fuentes de Agua"


class LightingType(models.Model):
    lighting_type = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.lighting_type

    class Meta:
        verbose_name = "Tipo de Iluminación"
        verbose_name_plural = "Tipos de Iluminación"


class WaterTreatment(models.Model):
    treatment_type = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.treatment_type

    class Meta:
        verbose_name = "Tipo de Tratamiento de Agua"
        verbose_name_plural = "Tipos de Tratamiento de Agua"


class WasteManagement(models.Model):
    management_type = models.CharField(max_length=50, blank=False, null=False, unique=True)
    biodegradable = models.BooleanField(default=False, help_text="¿El residuo es biodegradable?")
    recyclable = models.BooleanField(default=False, help_text="¿El residuo es reciclable?")
    non_recyclable = models.BooleanField(default=False, help_text="¿El residuo no es reciclable?")
    hazardous = models.BooleanField(default=False, help_text="¿El residuo es peligroso?")
    excreta = models.BooleanField(default=False, help_text="¿El residuo es excreta?")
    wastewater = models.BooleanField(default=False, help_text="¿El residuo es agua?")

    def __str__(self):
        return self.management_type

    class Meta:
        verbose_name = "Tipo de Manejo de Residuos"
        verbose_name_plural = "Tipos de Manejo de Residuos"


class MaterialConstructionFamilyCard(models.Model):
    family_card = models.ForeignKey(FamilyCard, on_delete=models.CASCADE, verbose_name="Ficha Familiar")
    material_roof = models.ForeignKey(MaterialConstruction, on_delete=models.CASCADE, related_name='roof_materials',
                                      verbose_name="Material de Techo")
    material_wall = models.ForeignKey(MaterialConstruction, on_delete=models.CASCADE, related_name='wall_materials',
                                      verbose_name="Material de Pared")
    material_floor = models.ForeignKey(MaterialConstruction, on_delete=models.CASCADE, related_name='floor_materials',
                                       verbose_name="Material de Piso")
    number_families = models.IntegerField(default=1, verbose_name="Número de Familias")
    number_people_bedrooms = models.IntegerField(default=1, verbose_name="Número de Personas por Habitación")
    condition_roof = models.CharField(max_length=50, blank=False, null=False, verbose_name="Condición del Techo")
    condition_wall = models.CharField(max_length=50, blank=False, null=False, verbose_name="Condición de la Pared")
    condition_floor = models.CharField(max_length=50, blank=False, null=False, verbose_name="Condición del Piso")
    home_ownership = models.ForeignKey(HomeOwnership, on_delete=models.CASCADE, verbose_name="Tipo de Propiedad")
    kitchen_location = models.IntegerField(default=1, verbose_name="Ubicación de la Cocina")
    cooking_fuel = models.ForeignKey(CookingFuel, on_delete=models.CASCADE,
                                     verbose_name="Tipo de Combustible de Cocina")
    home_smoke = models.BooleanField(default=False, verbose_name="Humo en la Vivienda",
                                     help_text="¿La vivienda tiene problemas de humo?")
    number_bedrooms = models.IntegerField(default=1, verbose_name="Número de Habitaciones")
    ventilation = models.BooleanField(default=False, verbose_name="Ventilación",
                                      help_text="¿La vivienda cuenta con ventilación adecuada?")
    lighting = models.BooleanField(default=False, verbose_name="Iluminación",
                                   help_text="¿La vivienda cuenta con iluminación adecuada?")

    def __str__(self):
        return f"Materiales de Construcción de la Vivienda {self.family_card.family_card_number}"

    class Meta:
        verbose_name = "Material de Construcción de Vivienda Familiar"
        verbose_name_plural = "Materiales de Construcción de Viviendas Familiares"
        unique_together = ('family_card', 'material_roof', 'material_wall', 'material_floor')

    def clean(self):
        if self.number_families <= 0:
            raise ValidationError("El número de familias debe ser mayor que cero.")
        if self.number_people_bedrooms <= 0:
            raise ValidationError("El número de personas por habitación debe ser mayor que cero.")
        if self.number_bedrooms <= 0:
            raise ValidationError("El número de habitaciones debe ser mayor que cero.")
        super().clean()

    def save(self, *args, **kwargs):
        self.condition_roof = self.condition_roof.strip().lower().capitalize() if self.condition_roof else ''
        self.condition_wall = self.condition_wall.strip().lower().capitalize() if self.condition_wall else ''
        self.condition_floor = self.condition_floor.strip().lower().capitalize() if self.condition_floor else ''
        super().save(*args, **kwargs)

    @classmethod
    def get_materials_by_family_card(cls, family_card_id):
        return cls.objects.filter(family_card_id=family_card_id).first()


class PublicServices(models.Model):
    family_card = models.ForeignKey(FamilyCard, on_delete=models.CASCADE, verbose_name="Ficha Familiar")
    water_service = models.BooleanField(default=False, verbose_name="Servicio de Agua",
                                        help_text="¿La vivienda cuenta con servicio de agua?")
    water_source = models.ForeignKey(WaterSource, on_delete=models.CASCADE, verbose_name="Fuente de Agua",
                                     help_text="Seleccione la fuente de agua utilizada en la vivienda")
    water_treatment = models.ForeignKey(WaterTreatment, on_delete=models.CASCADE, verbose_name="Tratamiento de Agua",
                                        help_text="Seleccione el tipo de tratamiento de agua utilizado en la vivienda")
    electricity_service = models.BooleanField(default=False, verbose_name="Servicio de Electricidad",
                                              help_text="¿La vivienda cuenta con servicio de electricidad?")
    sewage_service = models.BooleanField(default=False, verbose_name="Servicio de Alcantarillado",
                                         help_text="¿La vivienda cuenta con servicio de alcantarillado?")
    internet_service = models.BooleanField(default=False, verbose_name="Servicio de Internet",
                                           help_text="¿La vivienda cuenta con servicio de internet?")
    biodegradable_waste = models.ForeignKey(WasteManagement, on_delete=models.CASCADE, related_name='biodegradable_waste',
                                            verbose_name="Residuos Biodegradables",
                                           help_text="Seleccione el tipo de manejo de residuos biodegradables")
    recyclable_waste = models.ForeignKey(WasteManagement, on_delete=models.CASCADE, related_name='recyclable_waste',
                                         verbose_name="Residuos Reciclables",
                                         help_text="Seleccione el tipo de manejo de residuos reciclables")
    non_recyclable_waste = models.ForeignKey(WasteManagement, on_delete=models.CASCADE, related_name='non_recyclable_waste',
                                             verbose_name="Residuos No Reciclables",
                                             help_text="Seleccione el tipo de manejo de residuos no reciclables")
    hazardous_waste = models.ForeignKey(WasteManagement, on_delete=models.CASCADE, related_name='hazardous_waste',
                                        verbose_name="Residuos Peligrosos",
                                        help_text="Seleccione el tipo de manejo de residuos peligrosos")
    excreta_waste = models.ForeignKey(WasteManagement, on_delete=models.CASCADE, related_name='excreta_waste',
                                      verbose_name="Excreta",
                                      help_text="Seleccione el tipo de manejo de excreta")
    waste_water = models.ForeignKey(WasteManagement, on_delete=models.CASCADE, related_name='waste_water',
                                   verbose_name="Aguas Residuales",
                                   help_text="Seleccione el tipo de manejo de aguas residuales")


    def __str__(self):
        return f"Servicios Públicos de la Vivienda {self.family_card.family_card_number}"

    class Meta:
        verbose_name = "Servicios Públicos"
        verbose_name_plural = "Servicios Públicos"
        unique_together = ('family_card',)
