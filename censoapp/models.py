from django.db import models
from choices import handicap
# Create your models here.


class Association(models.Model):
    association_name = models.CharField(max_length=50, null=False, blank=False)
    association_identification = models.CharField(max_length=15, null=False, blank=False)
    association_type_document = models.CharField(max_length=3, null=False, blank=False, default='NIT',
                                                 help_text="Ingrese NIT")
    association_phone_mobile = models.CharField(max_length=15, help_text="Ingrese número de celular")
    association_phone = models.CharField(max_length=15)
    association_address = models.CharField(null=False, blank=False)
    association_departament = models.CharField(null=False, blank=False, max_length=15,
                                               help_text="Registre el departamento")
    association_email = models.EmailField(blank=False, null=False)
    association_logo = models.ImageField(null=False, blank=False, upload_to="Images")

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
    sidewalk_name = models.CharField(blank=False, null=False)
    organization_id = models.ForeignKey('Organizations', blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.sidewalk_name


class CivilState(models.Model):
    code_state_civil = models.CharField(blank=False, null=False, max_length=1)
    state_civil = models.CharField(blank=False, null=False)

    def __str__(self):
        return f"{self.code_state_civil} - {self.state_civil}"


class EducationLevel(models.Model):
    code_education_level = models.CharField(blank=False, null=False, max_length=1)
    education_level = models.CharField(blank=False, null=False, unique=True)

    def __str__(self):
        return self.education_level


class Eps(models.Model):
    code_eps = models.CharField(blank=False, null=False, unique=True)
    name_eps = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"{self.code_eps} - {self.name_eps}"


class Kinship(models.Model):
    code_kinship = models.CharField(blank=False, null=False, max_length=1)
    description_kinship = models.CharField(max_length=15, blank=False, null=False)

    def __str__(self):
        return self.description_kinship


class Occupancy(models.Model):
    description_occupancy = models.CharField(blank=False, null=False)

    def __str__(self):
        return self.description_occupancy


class DocumentType(models.Model):
    code_document_type = models.CharField(blank=False, null=False, unique=True, max_length=3)
    document_type = models.CharField(blank=False, null=False, max_length=15)

    def __str__(self):
        return f"{self.code_document_type} - {self.document_type}"


class Gender(models.Model):
    gender_code = models.CharField(blank=False, null=False)
    gender = models.CharField(blank=False, null=False)

    def __str__(self):
        return f"{self.gender_code} - {self.gender_code}"


class SecuritySocial(models.Model):
    code_security_social = models.CharField(blank=False, null=False, unique=True)
    affiliation = models.CharField(blank=False, null=False, max_length=30)

    def __str__(self):
        return f"{self.code_security_social} - {self.affiliation}"


class FamilyCard(models.Model):
    address_home = models.CharField(blank=False, null=False, help_text="Registre donde vive la familia")
    sidewalk_home = models.ForeignKey('Sidewalks', on_delete=models.CASCADE)
    latitude = models.CharField(default=0)
    length = models.CharField(default=0)
    ZONE = [(1, 'Rural'), (2, 'Urbana')]
    zone = models.CharField(choices=ZONE, blank=False, null=False)

    def __str__(self):
        return str(self.id) + '-' + self.address_home


class Person(models.Model):
    first_name_1 = models.CharField(blank=False, null=False, max_length=30)
    first_name_2 = models.CharField(blank=True, null=True, max_length=30)
    last_name_1 = models.CharField(blank=False, null=False, max_length=30)
    last_name_2 = models.CharField(blank=True, null=True, max_length=30)
    identification_person = models.CharField(blank=False, null=False, unique=True)
    document_type = models.ForeignKey('DocumentType', on_delete=models.CASCADE),
    cell_phone = models.CharField(blank=True, null=True)
    personal_email = models.EmailField(blank=True, null=True),
    gender_id = models.ForeignKey('Gender', on_delete=models.CASCADE)
    date_birth = models.DateField(blank=False, null=False)
    social_insurance = models.ForeignKey('SecuritySocial', on_delete=models.CASCADE,
                                         verbose_name="Seguridad Social")
    kinship_id = models.ForeignKey('Kinship', blank=False, null=False, on_delete=models.CASCADE,
                                   verbose_name="Parentesco")
    handicap = models.CharField(choices=handicap, default=7, verbose_name="Capacidades Diversas")
