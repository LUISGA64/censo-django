from django.db import models

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
    state_civil = models.CharField(blank=False, null=False)

    def __str__(self):
        return self.state_civil


class EducationLevel(models.Model):
    education_level = models.CharField(blank=False, null=False, unique=True)

    def __str__(self):
        return self.education_level


class Eps(models.Model):
    code_eps = models.CharField(blank=False, null=False, unique=True)
    name_eps = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"{self.code_eps} - {self.name_eps}"


class Kinship(models.Model):
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


class FamilyCard(models.Model):
    address_home = models.CharField(blank=False, null=False, help_text="Registre donde vive la familia")
    sidewalk_home = models.ForeignKey('Sidewalks', on_delete=models.CASCADE)
    latitude = models.CharField(default=0)
    length = models.CharField(default=0)

    def __str__(self):
        return str(self.id) + '-' + self.address_home


class Person(models.Model):
    first_name_1 = models.CharField(blank=False, null=False, max_length=30)
    first_name_2 = models.CharField(blank=True, null=True, max_length=30)
    last_name_1 = models.CharField(blank=False, null=False, max_length=30)
    last_name_2 = models.CharField(blank=True, null=True, max_length=30)
    identification_person = models.CharField(blank=False, null=False, unique=True)
    date_birth = models.DateField(blank=False, null=False)
