from django.db import models
from .choices import handicap, zone


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
    association_logo = models.ImageField(null=True, blank=False, upload_to="Association")

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
    organization_logo = models.ImageField(blank=False, null=False, upload_to="Images")
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


class SecuritySocial(models.Model):
    code_security_social = models.CharField(blank=False, null=False, unique=True, max_length=5)
    affiliation = models.CharField(blank=False, null=False, max_length=30)

    def __str__(self):
        return f"{self.affiliation}"


class FamilyCard(models.Model):

    address_home = models.CharField(blank=False, null=False, max_length=50, help_text="Registre donde vive la familia",
                                    verbose_name="Dirección Vivienda")
    sidewalk_home = models.ForeignKey('Sidewalks', on_delete=models.CASCADE, verbose_name="Vereda",
                                      help_text="Seleccione la vereda donde vive")
    latitude = models.CharField(default='0', max_length=15, help_text="Registre la latitud", verbose_name="Latitud")
    longitude = models.CharField(default='0', max_length=15, help_text="Registre la longitud", verbose_name="Longitud")
    zone = models.CharField(choices=zone, blank=False, null=False, max_length=10, help_text="Seleccione Urbana o Rural",
                            verbose_name="Zona")
    organization_id = models.ForeignKey('Organizations', on_delete=models.CASCADE, default='',
                                        verbose_name="Resguardo", help_text="Seleccione el Resguardo",
                                        null=False, blank=False)
    family_card_number = models.IntegerField(blank=False, null=False, unique=True, verbose_name="Número de Familia",
                                             default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Última Actualización")

    def __str__(self):
        return str(self.id) + '-' + self.address_home + '-' + str(self.sidewalk_home)


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

    gender_id = models.ForeignKey('Gender', on_delete=models.CASCADE, verbose_name="Género")

    date_birth = models.DateField(blank=False, null=False, verbose_name="Fecha de Nacimiento")

    social_insurance = models.ForeignKey('SecuritySocial', on_delete=models.CASCADE,
                                         verbose_name="Seguridad Social", max_length=50)

    eps = models.ForeignKey('Eps', on_delete=models.CASCADE, verbose_name="EPS")

    kinship_id = models.ForeignKey('Kinship', blank=False, null=False, on_delete=models.CASCADE,
                                   verbose_name="Parentescos")
    handicap = models.CharField(choices=handicap, max_length=50, verbose_name="Capacidades Diversas")

    education_level = models.ForeignKey('EducationLevel', on_delete=models.CASCADE, verbose_name="Nivel Educativo")

    civil_state = models.ForeignKey('CivilState', on_delete=models.CASCADE, verbose_name="Estado Civil")

    occupation = models.ForeignKey('Occupancy', blank=False, null=False, on_delete=models.CASCADE,
                                   verbose_name="Ocupación")
    family_card = models.ForeignKey('FamilyCard', on_delete=models.CASCADE, verbose_name="Familia", null=False,
                                    blank=False, default='')
    family_head = models.BooleanField(blank=False, null=False, default=False, verbose_name="Cabeza de Familia")
    state = models.BooleanField(blank=False, null=False, default=True, verbose_name="Estado")

    def __str__(self):
        return f"{self.first_name_1} {self.last_name_1} {self.identification_person}"
