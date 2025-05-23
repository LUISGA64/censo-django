from django.contrib import admin
from .models import (Association, Organizations, Sidewalks, DocumentType, Gender, Eps, Kinship, Occupancy, CivilState,
                     EducationLevel, SecuritySocial, Handicap)

# Register your models here.
admin.site.register(Association)
admin.site.register(Organizations)
admin.site.register(Sidewalks)
admin.site.register(DocumentType)
admin.site.register(Gender)
admin.site.register(Eps)
admin.site.register(Kinship)
admin.site.register(Occupancy)
admin.site.register(CivilState)
admin.site.register(EducationLevel)
admin.site.register(SecuritySocial)
admin.site.register(Handicap)
