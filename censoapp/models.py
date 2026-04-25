from django.core.exceptions import ValidationError
from django.db import models
from .choices import zone
from django.db.models import Max
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Importar modelos de seguridad
from .security_models import LoginAttempt, PasswordResetToken, SecurityEvent, SessionSecurity



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


class UserProfile(models.Model):
    """
    Perfil de usuario vinculado a una organizacion.
    Permite que cada usuario solo acceda a datos de su organizacion.
    Implementa multi-tenancy a nivel de aplicacion.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Usuario"
    )
    organization = models.ForeignKey(
        'Organizations',
        on_delete=models.CASCADE,
        verbose_name="Organizacion del Usuario",
        help_text="Organizacion a la que pertenece el usuario"
    )
    role = models.CharField(
        max_length=50,
        choices=[
            ('ADMIN', 'Administrador de Organizacion'),
            ('OPERATOR', 'Operador'),
            ('VIEWER', 'Solo Consulta')
        ],
        default='OPERATOR',
        verbose_name="Rol"
    )

    # Permisos especiales
    can_view_all_organizations = models.BooleanField(
        default=False,
        verbose_name="Acceso a todas las organizaciones",
        help_text="Solo para administradores de la asociacion. Permite ver datos de todas las organizaciones."
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el perfil esta activo"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualizacion")

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} - {self.organization.organization_name}"

    def has_permission_to_view_organization(self, organization):
        """
        Verifica si el usuario tiene permiso para ver datos de una organizacion especifica.
        """
        if self.user.is_superuser or self.can_view_all_organizations:
            return True
        return self.organization == organization


# Signal para crear perfil automaticamente al crear usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crea automaticamente un perfil cuando se crea un nuevo usuario.
    Si el usuario es superuser, se le da acceso a todas las organizaciones.
    """
    if created and not hasattr(instance, 'profile'):
        # Para superusuarios, crear perfil con acceso global
        if instance.is_superuser:
            # Obtener la primera organizacion o None
            first_org = Organizations.objects.first()
            if first_org:
                UserProfile.objects.create(
                    user=instance,
                    organization=first_org,
                    role='ADMIN',
                    can_view_all_organizations=True
                )
        # Para usuarios normales, se debe asignar organizacion manualmente desde admin


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Guarda el perfil cuando se guarda el usuario.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


class Sidewalks(models.Model):
    sidewalk_name = models.CharField(blank=False, null=False, max_length=40)
    organization_id = models.ForeignKey('Organizations', blank=False, null=False, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, help_text="Descripción de la vereda")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True,
                                   help_text="Latitud GPS (ej: 2.3167)")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True,
                                    help_text="Longitud GPS (ej: -76.4000)")

    def __str__(self):
        return self.sidewalk_name

    class Meta:
        verbose_name = "Vereda"
        verbose_name_plural = "Veredas"


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
    code_kinship = models.CharField(blank=False, null=False, max_length=2)
    description_kinship = models.CharField(max_length=25, blank=False, null=False)

    def __str__(self):
        return self.description_kinship


class Occupancy(models.Model):
    description_occupancy = models.CharField(blank=False, null=False, max_length=35)

    def __str__(self):
        return self.description_occupancy


class IdentificationDocumentType(models.Model):
    """Tipos de documentos de identificación personal (CC, TI, etc.)"""
    code_document_type = models.CharField(blank=False, null=False, unique=True, max_length=3)
    document_type = models.CharField(blank=False, null=False, max_length=25)

    def __str__(self):
        return f"{self.document_type}"

    class Meta:
        verbose_name = "Tipo de Documento de Identidad"
        verbose_name_plural = "Tipos de Documentos de Identidad"


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

    # Auditoría de cambios
    history = HistoricalRecords()

    class Meta:
        ordering = ['family_card_number']

    def __str__(self):
        return f"{self.id}"

    def clean(self):
        """Validar que el número de ficha sea válido"""
        from django.core.exceptions import ValidationError

        # Solo validar duplicados si el número NO es 0
        # Si es 0, se asignará automáticamente en save()
        if self.family_card_number and self.family_card_number != 0:
            duplicates = FamilyCard.objects.filter(
                family_card_number=self.family_card_number
            ).exclude(pk=self.pk)

            if duplicates.exists():
                raise ValidationError({
                    'family_card_number': f'El número de ficha {self.family_card_number} ya está en uso.'
                })

    def save(self, *args, **kwargs):
        # Normalizar dirección
        self.address_home = self.address_home.strip().lower().capitalize() if self.address_home else ''

        # Validar y asignar número de ficha si es necesario
        if not self.family_card_number or self.family_card_number == 0:
            self.family_card_number = self.get_next_family_card_number()

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
    document_type = models.ForeignKey('IdentificationDocumentType', on_delete=models.CASCADE, verbose_name="Tipo de documento",
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

    # Auditoría de cambios
    history = HistoricalRecords()

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
        # Normalizar campos de texto - manejar None y vacíos
        if self.first_name_1:
            self.first_name_1 = self.first_name_1.strip().lower().capitalize()
        if self.first_name_2:
            self.first_name_2 = self.first_name_2.strip().lower().capitalize()
        if self.last_name_1:
            self.last_name_1 = self.last_name_1.strip().lower().capitalize()
        if self.last_name_2:
            self.last_name_2 = self.last_name_2.strip().lower().capitalize()

        # Normalizar email y teléfono
        self.personal_email = self.personal_email.strip().lower() if self.personal_email else ''
        self.cell_phone = self.cell_phone.strip() if self.cell_phone else ''

        # Identificación siempre es requerida
        if self.identification_person:
            self.identification_person = self.identification_person.strip()

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
    main_charge = models.BooleanField(default=False,
                                      help_text="¿Este es el cargo principal?")

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
    """
    Modelo optimizado para almacenar características de construcción y vivienda.
    Solo puede existir un registro por ficha familiar.
    """
    family_card = models.OneToOneField(
        FamilyCard,
        on_delete=models.CASCADE,
        verbose_name="Ficha Familiar",
        unique=True,
        related_name='material_construction'
    )
    material_roof = models.ForeignKey(
        MaterialConstruction,
        on_delete=models.CASCADE,
        related_name='roof_materials',
        verbose_name="Material de Techo"
    )
    material_wall = models.ForeignKey(
        MaterialConstruction,
        on_delete=models.CASCADE,
        related_name='wall_materials',
        verbose_name="Material de Pared"
    )
    material_floor = models.ForeignKey(
        MaterialConstruction,
        on_delete=models.CASCADE,
        related_name='floor_materials',
        verbose_name="Material de Piso"
    )
    number_families = models.IntegerField(default=1, verbose_name="Número de Familias")
    number_people_bedrooms = models.IntegerField(default=1, verbose_name="Número de Personas por Habitación")
    condition_roof = models.CharField(max_length=50, blank=False, null=False, verbose_name="Condición del Techo")
    condition_wall = models.CharField(max_length=50, blank=False, null=False, verbose_name="Condición de la Pared")
    condition_floor = models.CharField(max_length=50, blank=False, null=False, verbose_name="Condición del Piso")
    home_ownership = models.ForeignKey(HomeOwnership, on_delete=models.CASCADE, verbose_name="Tipo de Propiedad")
    kitchen_location = models.IntegerField(default=1, verbose_name="Ubicación de la Cocina")
    cooking_fuel = models.ForeignKey(
        CookingFuel,
        on_delete=models.CASCADE,
        verbose_name="Tipo de Combustible de Cocina"
    )
    home_smoke = models.BooleanField(
        default=False,
        verbose_name="Humo en la Vivienda",
        help_text="¿La vivienda tiene problemas de humo?"
    )
    number_bedrooms = models.IntegerField(default=1, verbose_name="Número de Habitaciones")
    ventilation = models.BooleanField(
        default=False,
        verbose_name="Ventilación",
        help_text="¿La vivienda cuenta con ventilación adecuada?"
    )
    lighting = models.BooleanField(
        default=False,
        verbose_name="Iluminación",
        help_text="¿La vivienda cuenta con iluminación adecuada?"
    )

    # Auditoría de cambios
    history = HistoricalRecords()

    def __str__(self):
        return f"Materiales de Construcción de la Vivienda {self.family_card.family_card_number}"

    class Meta:
        verbose_name = "Material de Construcción de Vivienda Familiar"
        verbose_name_plural = "Materiales de Construcción de Viviendas Familiares"
        db_table = 'censoapp_materialconstructionfamilycard'

    def clean(self):
        """Validaciones a nivel de modelo"""
        if self.number_families <= 0:
            raise ValidationError("El número de familias debe ser mayor que cero.")
        if self.number_people_bedrooms <= 0:
            raise ValidationError("El número de personas por habitación debe ser mayor que cero.")
        if self.number_bedrooms <= 0:
            raise ValidationError("El número de habitaciones debe ser mayor que cero.")
        super().clean()

    def save(self, *args, **kwargs):
        """Normalizar campos de texto antes de guardar"""
        self.condition_roof = self.condition_roof.strip().capitalize() if self.condition_roof else ''
        self.condition_wall = self.condition_wall.strip().capitalize() if self.condition_wall else ''
        self.condition_floor = self.condition_floor.strip().capitalize() if self.condition_floor else ''
        self.full_clean()  # Ejecutar validaciones antes de guardar
        super().save(*args, **kwargs)

    @classmethod
    def get_materials_by_family_card(cls, family_card_id):
        """Obtener registro de materiales por ficha familiar (puede ser None)"""
        try:
            return cls.objects.get(family_card_id=family_card_id)
        except cls.DoesNotExist:
            return None


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



class DocumentType(models.Model):
    """
    Tipos de documentos que puede generar la organización.
    Ej: Aval, Constancia de Pertenencia, Certificado, etc.
    """
    document_type_name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=False,  # Temporal: remover unique para migración
        verbose_name="Tipo de Documento",
        default="Documento"  # Temporal para migración
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción del tipo de documento"
    )
    requires_expiration = models.BooleanField(
        default=True,
        verbose_name="Requiere Fecha de Vencimiento",
        help_text="¿Este tipo de documento tiene fecha de vencimiento?"
    )
    template_content = models.TextField(
        blank=True,
        null=True,
        verbose_name="Plantilla del Documento",
        help_text="Plantilla base del contenido del documento. Use {variables} para campos dinámicos."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        null=True,  # Temporal para migración
        blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización",
        null=True,  # Temporal para migración
        blank=True
    )

    def __str__(self):
        return self.document_type_name

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documentos"
        ordering = ['document_type_name']


class BoardPosition(models.Model):
    """
    Cargos de la Junta Directiva de la organización.
    Cada cargo puede tener un titular y un suplente.
    """
    POSITION_CHOICES = [
        ('GOBERNADOR', 'Gobernador'),
        ('ALCALDE', 'Alcalde'),
        ('CAPITAN', 'Capitán'),
        ('ALGUACIL', 'Alguacil'),
        ('COMISARIO', 'Comisario'),
        ('TESORERO', 'Tesorero'),
        ('SECRETARIO', 'Secretario'),
    ]

    organization = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        verbose_name="Organización",
        related_name='board_positions'
    )
    position_name = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
        verbose_name="Cargo",
        help_text="Cargo en la junta directiva"
    )

    # Titular del cargo
    holder_person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='board_position_holder',
        verbose_name="Titular del Cargo",
        help_text="Persona que ocupa el cargo como titular"
    )

    # Suplente del cargo
    alternate_person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='board_position_alternate',
        verbose_name="Suplente del Cargo",
        help_text="Persona que ocupa el cargo como suplente"
    )

    can_sign_documents = models.BooleanField(
        default=False,
        verbose_name="Autorizado para Firmar",
        help_text="¿Esta persona está autorizada para firmar documentos oficiales?"
    )

    start_date = models.DateField(
        verbose_name="Fecha de Inicio",
        help_text="Fecha en que inició en el cargo"
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Finalización",
        help_text="Fecha en que finalizó en el cargo (dejar vacío si está activo)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="¿El cargo está actualmente activo?"
    )

    observations = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización",
        null=True,
        blank=True
    )

    # Auditoría de cambios
    history = HistoricalRecords()

    def __str__(self):
        holder_name = self.holder_person.full_name if self.holder_person else "Sin asignar"
        return f"{self.get_position_name_display()} - {holder_name} ({self.organization.organization_name})"

    class Meta:
        verbose_name = "Cargo de Junta Directiva"
        verbose_name_plural = "Cargos de Junta Directiva"
        unique_together = [('organization', 'position_name', 'is_active')]
        ordering = ['organization', 'position_name']

    def clean(self):
        """Validaciones a nivel de modelo"""
        # Validar que el titular y suplente no sean la misma persona
        if self.holder_person and self.alternate_person:
            if self.holder_person == self.alternate_person:
                raise ValidationError("El titular y el suplente no pueden ser la misma persona.")

        # Validar que la persona pertenezca a la misma organización
        if self.holder_person:
            if self.holder_person.family_card.organization != self.organization:
                raise ValidationError(
                    f"El titular {self.holder_person.full_name} no pertenece a la organización {self.organization.organization_name}"
                )

        if self.alternate_person:
            if self.alternate_person.family_card.organization != self.organization:
                raise ValidationError(
                    f"El suplente {self.alternate_person.full_name} no pertenece a la organización {self.organization.organization_name}"
                )

        # Validar fechas
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValidationError("La fecha de finalización no puede ser anterior a la fecha de inicio.")

        # Validar que no exista otro cargo activo con el mismo cargo en la organización
        if self.is_active:
            existing = BoardPosition.objects.filter(
                organization=self.organization,
                position_name=self.position_name,
                is_active=True
            )
            if self.pk:
                existing = existing.exclude(pk=self.pk)

            if existing.exists():
                raise ValidationError(
                    f"Ya existe un cargo activo de {self.get_position_name_display()} en {self.organization.organization_name}"
                )

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def is_valid_on_date(self, check_date):
        """
        Verifica si el cargo está vigente en una fecha específica.

        Args:
            check_date: Fecha a verificar (date object)

        Returns:
            bool: True si el cargo está vigente en esa fecha
        """
        # Debe estar marcado como activo
        if not self.is_active:
            return False

        # La fecha debe ser >= fecha de inicio
        if check_date < self.start_date:
            return False

        # Si hay fecha de fin, la fecha debe ser <= fecha de fin
        if self.end_date and check_date > self.end_date:
            return False

        return True

    @classmethod
    def get_valid_positions_on_date(cls, organization, check_date):
        """
        Obtiene todos los cargos vigentes de una organización en una fecha específica.

        Args:
            organization: Organización
            check_date: Fecha a verificar

        Returns:
            QuerySet de BoardPosition vigentes
        """
        positions = cls.objects.filter(
            organization=organization,
            is_active=True,
            start_date__lte=check_date
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=check_date)
        )
        return positions

    @classmethod
    def get_signers_on_date(cls, organization, check_date):
        """
        Obtiene los cargos autorizados para firmar en una fecha específica.

        Args:
            organization: Organización
            check_date: Fecha a verificar

        Returns:
            QuerySet de BoardPosition autorizados a firmar
        """
        return cls.get_valid_positions_on_date(organization, check_date).filter(
            can_sign_documents=True
        )


class GeneratedDocument(models.Model):
    """
    Documentos generados por la organización para personas del censo.
    Reemplaza el antiguo modelo AvalGenerated con un sistema más completo.
    """
    # Tipo de documento
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        verbose_name="Tipo de Documento",
        help_text="Tipo de documento a generar (Aval, Constancia, etc.)"
    )

    # Persona beneficiaria del documento
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name="Persona Beneficiaria",
        help_text="Persona del censo para quien se genera el documento",
        related_name='documents_received'
    )

    # Organización que expide el documento
    organization = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        verbose_name="Organización que Expide",
        help_text="Organización que genera y expide el documento"
    )

    # Contenido del documento
    document_content = models.TextField(
        verbose_name="Contenido del Documento",
        help_text="Contenido completo del documento generado"
    )

    # Fecha de generación y vigencia
    issue_date = models.DateField(
        verbose_name="Fecha de Expedición",
        help_text="Fecha en que se expide el documento"
    )
    expiration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Vencimiento",
        help_text="Fecha de vencimiento del documento (si aplica)"
    )

    # Número de documento (consecutivo)
    document_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número de Documento",
        help_text="Número consecutivo del documento"
    )

    # Hash de verificación para código QR
    verification_hash = models.CharField(
        max_length=64,  # SHA-256 genera 64 caracteres hexadecimales
        blank=True,
        null=True,
        unique=True,
        verbose_name="Hash de Verificación",
        help_text="Hash único para verificar autenticidad del documento vía código QR"
    )

    # Firmantes del documento (miembros de la junta directiva)
    signers = models.ManyToManyField(
        BoardPosition,
        verbose_name="Firmantes",
        help_text="Miembros de la junta directiva que firman el documento",
        related_name='signed_documents',
        blank=True
    )

    # Estado del documento
    STATUS_CHOICES = [
        ('DRAFT', 'Borrador'),
        ('ISSUED', 'Expedido'),
        ('EXPIRED', 'Vencido'),
        ('REVOKED', 'Revocado'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT',
        verbose_name="Estado"
    )

    # Observaciones y notas
    observations = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )

    # Usuario que generó el documento
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Creado por",
        related_name='documents_created'
    )

    # Auditoría
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización",
        null=True,
        blank=True
    )

    # Auditoría de cambios
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.document_type.document_type_name} - {self.person.full_name} ({self.document_number or 'S/N'})"

    class Meta:
        verbose_name = "Documento Generado"
        verbose_name_plural = "Documentos Generados"
        ordering = ['-created_at']

    def clean(self):
        """Validaciones a nivel de modelo"""
        # Validar que la persona pertenezca a la organización que expide
        if self.person and self.organization:
            if self.person.family_card.organization != self.organization:
                raise ValidationError(
                    f"La persona {self.person.full_name} no pertenece a la organización {self.organization.organization_name}"
                )

        # Validar fecha de vencimiento
        if self.expiration_date and self.issue_date:
            if self.expiration_date < self.issue_date:
                raise ValidationError("La fecha de vencimiento no puede ser anterior a la fecha de expedición.")

        # Validar que si el tipo de documento requiere vencimiento, se proporcione
        if self.document_type and self.document_type.requires_expiration:
            if not self.expiration_date:
                raise ValidationError(
                    f"El tipo de documento '{self.document_type.document_type_name}' requiere fecha de vencimiento."
                )

        # VALIDACIÓN CRÍTICA: Verificar que exista junta directiva vigente en la fecha de expedición
        if self.issue_date and self.organization:
            # Obtener cargos vigentes en la fecha de expedición
            valid_positions = BoardPosition.get_valid_positions_on_date(
                self.organization,
                self.issue_date
            )

            if not valid_positions.exists():
                raise ValidationError(
                    f"No existe una junta directiva vigente para la organización '{self.organization.organization_name}' "
                    f"en la fecha de expedición ({self.issue_date.strftime('%Y-%m-%d')}). "
                    f"No se pueden generar documentos sin una junta directiva activa."
                )

            # Verificar que existan firmantes autorizados en esa fecha
            valid_signers = BoardPosition.get_signers_on_date(
                self.organization,
                self.issue_date
            )

            if not valid_signers.exists():
                raise ValidationError(
                    f"No hay miembros de la junta directiva autorizados para firmar documentos "
                    f"en la fecha de expedición ({self.issue_date.strftime('%Y-%m-%d')}). "
                    f"Debe existir al menos un cargo con permiso para firmar."
                )

        super().clean()

    def save(self, *args, **kwargs):
        # Generar número de documento si no existe
        if not self.document_number:
            from datetime import datetime
            year = datetime.now().year
            # Contar documentos del mismo tipo en el año actual
            count = GeneratedDocument.objects.filter(
                document_type=self.document_type,
                organization=self.organization,
                created_at__year=year
            ).count() + 1

            # Formato: TIPO-ORG-AÑO-###
            doc_type_abbr = self.document_type.document_type_name[:3].upper()
            org_abbr = self.organization.organization_name[:3].upper()
            self.document_number = f"{doc_type_abbr}-{org_abbr}-{year}-{count:04d}"

        # Actualizar estado si está vencido
        if self.expiration_date:
            from datetime import date
            if self.expiration_date < date.today() and self.status == 'ISSUED':
                self.status = 'EXPIRED'

        self.full_clean()

        # Guardar primero para tener un ID si es nuevo
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Generar hash de verificación si no existe (después de guardar para tener ID)
        if not self.verification_hash:
            import hashlib
            verification_data = f"{self.id}|{self.document_number}|{self.issue_date.isoformat()}"
            self.verification_hash = hashlib.sha256(verification_data.encode()).hexdigest()[:16]
            # Guardar solo el hash sin trigger validaciones de nuevo
            GeneratedDocument.objects.filter(pk=self.pk).update(verification_hash=self.verification_hash)

    @classmethod
    def get_active_documents_for_person(cls, person):
        """Obtener documentos activos de una persona"""
        from datetime import date
        return cls.objects.filter(
            person=person,
            status='ISSUED',
            expiration_date__gte=date.today()
        )

    @property
    def is_expired(self):
        """Verifica si el documento está vencido"""
        if not self.expiration_date:
            return False
        from datetime import date
        return self.expiration_date < date.today()

    @property
    def days_until_expiration(self):
        """Días hasta el vencimiento"""
        if not self.expiration_date:
            return None
        from datetime import date
        delta = self.expiration_date - date.today()
        return delta.days if delta.days > 0 else 0

    def validate_signers(self):
        """
        Valida que todos los firmantes asignados estén vigentes en la fecha de expedición.
        Este método se debe llamar después de asignar los firmantes (ManyToMany).
        """
        if not self.issue_date:
            return

        invalid_signers = []
        for signer in self.signers.all():
            if not signer.is_valid_on_date(self.issue_date):
                invalid_signers.append(signer)

        if invalid_signers:
            signer_names = ", ".join([
                f"{s.get_position_name_display()} ({s.holder_person.full_name if s.holder_person else 'Sin asignar'})"
                for s in invalid_signers
            ])
            raise ValidationError(
                f"Los siguientes firmantes NO están vigentes en la fecha de expedición "
                f"({self.issue_date.strftime('%Y-%m-%d')}): {signer_names}. "
                f"Solo pueden firmar miembros de la junta directiva que estén en funciones en esa fecha."
            )

        # Validar que todos los firmantes puedan firmar documentos
        unauthorized_signers = []
        for signer in self.signers.all():
            if not signer.can_sign_documents:
                unauthorized_signers.append(signer)

        if unauthorized_signers:
            signer_names = ", ".join([
                f"{s.get_position_name_display()}"
                for s in unauthorized_signers
            ])
            raise ValidationError(
                f"Los siguientes cargos NO están autorizados para firmar documentos: {signer_names}. "
                f"Debe marcar el permiso 'Autorizado para Firmar' en el cargo."
            )


# ========================================
# MODELOS DE PLANTILLAS DE DOCUMENTOS
# Sistema de plantillas personalizables por organización
# ========================================

class DocumentTemplate(models.Model):
    """
    Plantillas personalizables para documentos de cada organización.
    Permite configurar estructura, estilos, logos, contenido, etc.
    """
    # Relación con organización y tipo de documento
    organization = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        verbose_name="Organización",
        help_text="Organización propietaria de esta plantilla",
        related_name='document_templates'
    )

    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        verbose_name="Tipo de Documento",
        help_text="Tipo de documento al que aplica esta plantilla",
        related_name='templates'
    )

    # Información básica de la plantilla
    name = models.CharField(
        max_length=200,
        verbose_name="Nombre de la Plantilla",
        help_text="Nombre descriptivo (ej: 'Aval Comunitario v2')"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción del propósito de esta plantilla"
    )

    version = models.CharField(
        max_length=20,
        default='1.0',
        verbose_name="Versión",
        help_text="Versión de la plantilla (ej: 1.0, 2.1)"
    )

    # Estado y activación
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Si está activa, se usará para generar documentos"
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name="Plantilla por Defecto",
        help_text="Si es la plantilla predeterminada para este tipo de documento"
    )

    # ========================================
    # CONFIGURACIÓN DE DISEÑO
    # ========================================

    # Logo de la organización
    logo_position = models.CharField(
        max_length=20,
        choices=[
            ('top-left', 'Superior Izquierda'),
            ('top-center', 'Superior Centro'),
            ('top-right', 'Superior Derecha'),
            ('none', 'Sin Logo'),
        ],
        default='top-left',
        verbose_name="Posición del Logo"
    )

    logo_width = models.IntegerField(
        default=100,
        verbose_name="Ancho del Logo (px)",
        help_text="Ancho del logo en píxeles"
    )

    # Encabezado
    show_organization_info = models.BooleanField(
        default=True,
        verbose_name="Mostrar Info Organización en Encabezado",
        help_text="Muestra nombre, NIT, dirección, etc."
    )

    organization_info_position = models.CharField(
        max_length=20,
        choices=[
            ('top-left', 'Superior Izquierda'),
            ('top-center', 'Superior Centro'),
            ('top-right', 'Superior Derecha'),
        ],
        default='top-right',
        verbose_name="Posición Info Organización"
    )

    header_custom_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Texto Personalizado Encabezado",
        help_text="Texto adicional en el encabezado (acepta HTML)"
    )

    # ========================================
    # CONTENIDO DEL DOCUMENTO
    # ========================================

    # Título del documento
    document_title = models.CharField(
        max_length=200,
        default='CERTIFICADO',
        verbose_name="Título del Documento",
        help_text="Título principal (ej: 'CERTIFICADO', 'CONSTANCIA')"
    )

    title_alignment = models.CharField(
        max_length=20,
        choices=[
            ('left', 'Izquierda'),
            ('center', 'Centro'),
            ('right', 'Derecha'),
        ],
        default='center',
        verbose_name="Alineación del Título"
    )

    # Introducción/Encabezado del contenido
    introduction_text = models.TextField(
        default='LA JUNTA DIRECTIVA DE {organizacion}',
        verbose_name="Texto de Introducción",
        help_text="Texto introductorio (puede usar variables con {})"
    )

    introduction_bold = models.BooleanField(
        default=True,
        verbose_name="Introducción en Negrita"
    )

    # Cuerpo principal (estructura JSON para bloques)
    content_blocks = models.JSONField(
        default=list,
        verbose_name="Bloques de Contenido",
        help_text="Estructura JSON con bloques de contenido configurables"
    )

    # Cierre/Despedida
    closing_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Texto de Cierre",
        help_text="Texto de cierre del documento"
    )

    # ========================================
    # PIE DE PÁGINA Y FIRMAS
    # ========================================

    show_signatures = models.BooleanField(
        default=True,
        verbose_name="Mostrar Firmas",
        help_text="Muestra espacios para firmas de la junta directiva"
    )

    signature_layout = models.CharField(
        max_length=20,
        choices=[
            ('horizontal', 'Horizontal (todas en una fila)'),
            ('two-columns', 'Dos Columnas'),
            ('vertical', 'Vertical (una debajo de otra)'),
        ],
        default='two-columns',
        verbose_name="Diseño de Firmas"
    )

    show_qr_code = models.BooleanField(
        default=True,
        verbose_name="Mostrar Código QR",
        help_text="Incluye código QR para verificación"
    )

    qr_position = models.CharField(
        max_length=20,
        choices=[
            ('bottom-left', 'Inferior Izquierda'),
            ('bottom-center', 'Inferior Centro'),
            ('bottom-right', 'Inferior Derecha'),
        ],
        default='bottom-right',
        verbose_name="Posición del QR"
    )

    footer_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Texto del Pie de Página",
        help_text="Texto adicional en el pie de página"
    )

    # ========================================
    # ESTILOS Y PERSONALIZACIÓN
    # ========================================

    # Colores
    primary_color = models.CharField(
        max_length=7,
        default='#2196F3',
        verbose_name="Color Primario",
        help_text="Color principal (formato hexadecimal #RRGGBB)"
    )

    secondary_color = models.CharField(
        max_length=7,
        default='#1976D2',
        verbose_name="Color Secundario",
        help_text="Color secundario (formato hexadecimal #RRGGBB)"
    )

    text_color = models.CharField(
        max_length=7,
        default='#000000',
        verbose_name="Color del Texto",
        help_text="Color del texto principal"
    )

    # Fuentes
    font_family = models.CharField(
        max_length=100,
        default='Arial, sans-serif',
        verbose_name="Familia de Fuente",
        help_text="Fuente del documento (ej: Arial, Times New Roman)"
    )

    font_size = models.IntegerField(
        default=12,
        verbose_name="Tamaño de Fuente Base (pt)",
        help_text="Tamaño base de la fuente en puntos"
    )

    # Márgenes (en milímetros)
    margin_top = models.IntegerField(
        default=25,
        verbose_name="Margen Superior (mm)"
    )

    margin_bottom = models.IntegerField(
        default=25,
        verbose_name="Margen Inferior (mm)"
    )

    margin_left = models.IntegerField(
        default=25,
        verbose_name="Margen Izquierdo (mm)"
    )

    margin_right = models.IntegerField(
        default=25,
        verbose_name="Margen Derecho (mm)"
    )

    # Tamaño de página
    page_size = models.CharField(
        max_length=20,
        choices=[
            ('A4', 'A4 (210 × 297 mm)'),
            ('Letter', 'Carta (216 × 279 mm)'),
            ('Legal', 'Oficio (216 × 356 mm)'),
        ],
        default='A4',
        verbose_name="Tamaño de Página"
    )

    page_orientation = models.CharField(
        max_length=20,
        choices=[
            ('portrait', 'Vertical'),
            ('landscape', 'Horizontal'),
        ],
        default='portrait',
        verbose_name="Orientación de Página"
    )

    # ========================================
    # CSS Y HTML PERSONALIZADO
    # ========================================

    custom_css = models.TextField(
        blank=True,
        null=True,
        verbose_name="CSS Personalizado",
        help_text="Estilos CSS adicionales para personalización avanzada"
    )

    custom_html = models.TextField(
        blank=True,
        null=True,
        verbose_name="HTML Personalizado",
        help_text="HTML adicional para estructura personalizada"
    )

    # ========================================
    # METADATOS Y AUDITORÍA
    # ========================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='templates_created',
        verbose_name="Creado Por"
    )

    last_modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='templates_modified',
        verbose_name="Última Modificación Por"
    )

    # Historial de cambios
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Plantilla de Documento"
        verbose_name_plural = "Plantillas de Documentos"
        ordering = ['-is_default', '-is_active', 'organization', 'document_type', 'name']
        unique_together = [
            ['organization', 'document_type', 'name'],
        ]
        indexes = [
            models.Index(fields=['organization', 'document_type', 'is_active']),
            models.Index(fields=['is_default', 'is_active']),
        ]

    def __str__(self):
        return f"{self.organization.organization_name} - {self.document_type.document_type_name} - {self.name}"

    def save(self, *args, **kwargs):
        """Override save para asegurar que solo haya una plantilla por defecto"""
        if self.is_default:
            DocumentTemplate.objects.filter(
                organization=self.organization,
                document_type=self.document_type,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)

        super().save(*args, **kwargs)


class TemplateBlock(models.Model):
    """Bloques de contenido para plantillas"""
    template = models.ForeignKey(
        DocumentTemplate,
        on_delete=models.CASCADE,
        related_name='blocks',
        verbose_name="Plantilla"
    )

    BLOCK_TYPES = [
        ('text', 'Texto'),
        ('paragraph', 'Párrafo'),
        ('list', 'Lista'),
        ('table', 'Tabla'),
        ('image', 'Imagen'),
        ('spacer', 'Espaciador'),
        ('divider', 'Divisor'),
        ('custom', 'HTML Personalizado'),
    ]

    block_type = models.CharField(
        max_length=20,
        choices=BLOCK_TYPES,
        verbose_name="Tipo de Bloque"
    )

    order = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición en el documento"
    )

    content = models.TextField(
        verbose_name="Contenido",
        help_text="Contenido del bloque (puede contener variables)"
    )

    # Estilos del bloque
    is_bold = models.BooleanField(default=False, verbose_name="Negrita")
    is_italic = models.BooleanField(default=False, verbose_name="Cursiva")
    is_underline = models.BooleanField(default=False, verbose_name="Subrayado")

    alignment = models.CharField(
        max_length=20,
        choices=[
            ('left', 'Izquierda'),
            ('center', 'Centro'),
            ('right', 'Derecha'),
            ('justify', 'Justificado'),
        ],
        default='justify',
        verbose_name="Alineación"
    )

    font_size_modifier = models.IntegerField(
        default=0,
        verbose_name="Modificador de Tamaño",
        help_text="Suma/resta al tamaño base de fuente"
    )

    custom_style = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Estilo CSS Personalizado"
    )

    config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Configuración del Bloque"
    )

    class Meta:
        verbose_name = "Bloque de Plantilla"
        verbose_name_plural = "Bloques de Plantilla"
        ordering = ['template', 'order']

    def __str__(self):
        return f"{self.template.name} - {self.get_block_type_display()} #{self.order}"


class TemplateVariable(models.Model):
    """
    Variables personalizadas adicionales que puede definir cada organización.
    Basadas en campos de modelos (Persona, Ficha Familiar, Asociación, Organización)
    """

    VARIABLE_TYPES = [
        ('person', 'Dato de Persona'),
        ('family_card', 'Dato de Ficha Familiar'),
        ('association', 'Dato de Asociación'),
        ('organization', 'Dato de Organización'),
    ]

    organization = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        related_name='custom_variables',
        verbose_name="Organización"
    )

    variable_name = models.CharField(
        max_length=100,
        verbose_name="Nombre de la Variable",
        help_text="Nombre único sin llaves (ej: 'territorio', 'nombre_completo')"
    )

    variable_type = models.CharField(
        max_length=20,
        choices=VARIABLE_TYPES,
        verbose_name="Tipo de Variable",
        help_text="Tipo de dato (Persona, Ficha Familiar, Asociación, Organización)"
    )

    variable_value = models.CharField(
        max_length=200,
        verbose_name="Campo del Modelo",
        help_text="Nombre del campo del modelo (ej: 'organization_territory', 'full_name')"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción del propósito de esta variable"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )

    class Meta:
        verbose_name = "Variable Personalizada"
        verbose_name_plural = "Variables Personalizadas"
        unique_together = [['organization', 'variable_name']]
        ordering = ['organization', 'variable_type', 'variable_name']

    def __str__(self):
        return f"{{{self.variable_name}}} = {self.get_variable_type_display()}.{self.variable_value}"

    @property
    def full_variable_name(self):
        """Retorna el nombre de la variable con llaves"""
        return f"{{{self.variable_name}}}"

    def get_value(self, person=None, organization=None, family_card=None):
        """
        Obtiene el valor de la variable según su tipo.

        Args:
            person: Instancia de Person (opcional)
            organization: Instancia de Organizations (opcional)
            family_card: Instancia de FamilyCard (opcional)

        Returns:
            str: Valor de la variable
        """
        if self.variable_type == 'static':
            # Valor estático directo
            return self.variable_value

        elif self.variable_type == 'organization':
            # Obtener dato de la organización
            if organization:
                return self._get_model_field(organization, self.variable_value)
            elif self.organization:
                return self._get_model_field(self.organization, self.variable_value)
            return ''

        elif self.variable_type == 'person':
            # Obtener dato de la persona
            if person:
                return self._get_model_field(person, self.variable_value)
            return ''

        elif self.variable_type == 'family_card':
            # Obtener dato de la ficha familiar
            card = family_card
            if not card and person:
                card = person.family_card
            if card:
                return self._get_model_field(card, self.variable_value)
            return ''

        return self.variable_value

    def _get_model_field(self, obj, field_path):
        """
        Obtiene el valor de un campo del modelo, soportando relaciones con punto.

        Args:
            obj: Instancia del modelo
            field_path: Ruta al campo (ej: 'organization_name', 'sidewalk_home.sidewalk_name')

        Returns:
            str: Valor del campo
        """
        try:
            # Soportar campos con relaciones (ej: sidewalk_home.sidewalk_name)
            parts = field_path.split('.')
            value = obj

            for part in parts:
                if hasattr(value, part):
                    value = getattr(value, part)
                    # Si es un método, llamarlo
                    if callable(value):
                        value = value()
                else:
                    return ''

            # Convertir a string
            return str(value) if value is not None else ''
        except Exception as e:
            print(f"Error obteniendo campo {field_path}: {e}")
            return ''


# ============================================================================
# SISTEMA DE NOTIFICACIONES
# ============================================================================

class NotificationType(models.TextChoices):
    """Tipos de notificaciones disponibles"""
    DOCUMENT_EXPIRING = 'DOC_EXP', 'Documento por vencer'
    DOCUMENT_EXPIRED = 'DOC_EXPD', 'Documento vencido'
    DOCUMENT_GENERATED = 'DOC_GEN', 'Documento generado'
    PERSON_CREATED = 'PER_NEW', 'Persona registrada'
    PERSON_UPDATED = 'PER_UPD', 'Persona actualizada'
    FAMILY_CREATED = 'FAM_NEW', 'Familia registrada'
    FAMILY_UPDATED = 'FAM_UPD', 'Familia actualizada'
    SYSTEM_UPDATE = 'SYS_UPD', 'Actualización del sistema'
    SYSTEM_ERROR = 'SYS_ERR', 'Error del sistema'
    SECURITY_ALERT = 'SEC_ALT', 'Alerta de seguridad'
    CUSTOM = 'CUSTOM', 'Personalizada'


class Notification(models.Model):
    """
    Modelo para notificaciones del sistema.
    Soporta notificaciones in-app y email.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="Usuario que recibe la notificación"
    )

    organization = models.ForeignKey(
        'Organizations',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Organización relacionada"
    )

    notification_type = models.CharField(
        max_length=10,
        choices=NotificationType.choices,
        default=NotificationType.CUSTOM,
        help_text="Tipo de notificación"
    )

    title = models.CharField(
        max_length=200,
        help_text="Título de la notificación"
    )

    message = models.TextField(
        help_text="Mensaje de la notificación"
    )

    link = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL para redireccionar (opcional)"
    )

    is_read = models.BooleanField(
        default=False,
        help_text="Indica si la notificación ha sido leída"
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha y hora en que fue leída"
    )

    sent_email = models.BooleanField(
        default=False,
        help_text="Indica si se envió email"
    )

    email_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha y hora de envío de email"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Última actualización"
    )

    # Campos adicionales para contexto
    related_person = models.ForeignKey(
        'Person',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Persona relacionada (opcional)"
    )

    related_document = models.ForeignKey(
        'GeneratedDocument',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Documento relacionado (opcional)"
    )

    related_family = models.ForeignKey(
        'FamilyCard',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Ficha familiar relacionada (opcional)"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['notification_type']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def mark_as_read(self):
        """Marca la notificación como leída"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def get_icon(self):
        """Retorna el icono correspondiente al tipo de notificación"""
        icons = {
            NotificationType.DOCUMENT_EXPIRING: 'fa-clock',
            NotificationType.DOCUMENT_EXPIRED: 'fa-exclamation-triangle',
            NotificationType.DOCUMENT_GENERATED: 'fa-file-pdf',
            NotificationType.PERSON_CREATED: 'fa-user-plus',
            NotificationType.PERSON_UPDATED: 'fa-user-edit',
            NotificationType.FAMILY_CREATED: 'fa-home',
            NotificationType.FAMILY_UPDATED: 'fa-edit',
            NotificationType.SYSTEM_UPDATE: 'fa-info-circle',
            NotificationType.SYSTEM_ERROR: 'fa-exclamation-circle',
            NotificationType.SECURITY_ALERT: 'fa-shield-alt',
            NotificationType.CUSTOM: 'fa-bell',
        }
        return icons.get(self.notification_type, 'fa-bell')

    def get_color(self):
        """Retorna el color correspondiente al tipo de notificación"""
        colors = {
            NotificationType.DOCUMENT_EXPIRING: 'warning',
            NotificationType.DOCUMENT_EXPIRED: 'danger',
            NotificationType.DOCUMENT_GENERATED: 'success',
            NotificationType.PERSON_CREATED: 'info',
            NotificationType.PERSON_UPDATED: 'info',
            NotificationType.FAMILY_CREATED: 'primary',
            NotificationType.FAMILY_UPDATED: 'primary',
            NotificationType.SYSTEM_UPDATE: 'info',
            NotificationType.SYSTEM_ERROR: 'danger',
            NotificationType.SECURITY_ALERT: 'danger',
            NotificationType.CUSTOM: 'secondary',
        }
        return colors.get(self.notification_type, 'secondary')


class NotificationPreference(models.Model):
    """
    Preferencias de notificación por usuario.
    Permite a cada usuario configurar qué notificaciones desea recibir.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        help_text="Usuario"
    )

    # Canales de notificación
    receive_email = models.BooleanField(
        default=True,
        help_text="Recibir notificaciones por email"
    )

    receive_inapp = models.BooleanField(
        default=True,
        help_text="Recibir notificaciones in-app"
    )

    # Tipos de notificaciones
    notify_document_expiring = models.BooleanField(
        default=True,
        help_text="Notificar documentos por vencer"
    )

    notify_document_expired = models.BooleanField(
        default=True,
        help_text="Notificar documentos vencidos"
    )

    notify_document_generated = models.BooleanField(
        default=False,
        help_text="Notificar documentos generados"
    )

    notify_person_created = models.BooleanField(
        default=False,
        help_text="Notificar nuevas personas"
    )

    notify_family_created = models.BooleanField(
        default=False,
        help_text="Notificar nuevas familias"
    )

    notify_system_updates = models.BooleanField(
        default=True,
        help_text="Notificar actualizaciones del sistema"
    )

    notify_security_alerts = models.BooleanField(
        default=True,
        help_text="Notificar alertas de seguridad"
    )

    # Frecuencia
    email_frequency = models.CharField(
        max_length=10,
        choices=[
            ('INSTANT', 'Inmediato'),
            ('DAILY', 'Diario'),
            ('WEEKLY', 'Semanal'),
            ('NEVER', 'Nunca'),
        ],
        default='INSTANT',
        help_text="Frecuencia de envío de emails"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Preferencia de Notificación'
        verbose_name_plural = 'Preferencias de Notificación'

    def __str__(self):
        return f"Preferencias de {self.user.username}"


# Signal para crear preferencias automáticamente al crear usuario
@receiver(post_save, sender=User)
def create_notification_preferences(sender, instance, created, **kwargs):
    """Crea preferencias de notificación para nuevos usuarios"""
    if created:
        NotificationPreference.objects.get_or_create(user=instance)

