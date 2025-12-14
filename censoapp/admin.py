from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (Association, Organizations, Sidewalks, DocumentType, Gender, Eps, Kinship, Occupancy, CivilState,
                     EducationLevel, SecuritySocial, Handicap, Charge, SystemParameters, MaterialConstruction,
                     WaterTreatment, LightingType, WaterSource, CookingFuel, HomeOwnership, FamilyCard, Person,
                     MaterialConstructionFamilyCard, UserProfile)
from .utils import invalidate_system_parameters_cache

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
admin.site.register(Charge)
# SystemParameters se registra mas abajo con admin personalizado
admin.site.register(MaterialConstruction)
admin.site.register(HomeOwnership)
admin.site.register(WaterTreatment)
admin.site.register(LightingType)
admin.site.register(WaterSource)
admin.site.register(CookingFuel)


# SystemParameters con invalidacion automatica de cache
@admin.register(SystemParameters)
class SystemParametersAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
    search_fields = ['key', 'value']
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        """Invalida cache al guardar"""
        super().save_model(request, obj, form, change)
        invalidate_system_parameters_cache()
        self.message_user(request, f"Parametro '{obj.key}' guardado. Cache invalidado.", level='SUCCESS')

    def delete_model(self, request, obj):
        """Invalida cache al eliminar"""
        key = obj.key
        super().delete_model(request, obj)
        invalidate_system_parameters_cache()
        self.message_user(request, f"Parametro '{key}' eliminado. Cache invalidado.", level='SUCCESS')

    def delete_queryset(self, request, queryset):
        """Invalida cache al eliminar multiples"""
        count = queryset.count()
        super().delete_queryset(request, queryset)
        invalidate_system_parameters_cache()
        self.message_user(request, f"{count} parametros eliminados. Cache invalidado.", level='SUCCESS')


# Modelos con auditoria usando SimpleHistoryAdmin
@admin.register(FamilyCard)
class FamilyCardAdmin(SimpleHistoryAdmin):
    list_display = ['family_card_number', 'sidewalk_home', 'zone', 'organization', 'state', 'created_at']
    list_filter = ['zone', 'state', 'organization']
    search_fields = ['family_card_number', 'address_home']
    history_list_display = ['state', 'zone']

@admin.register(Person)
class PersonAdmin(SimpleHistoryAdmin):
    list_display = ['identification_person', 'first_name_1', 'last_name_1', 'family_head', 'state', 'family_card']
    list_filter = ['family_head', 'state', 'gender']
    search_fields = ['identification_person', 'first_name_1', 'last_name_1']
    history_list_display = ['family_head', 'state']

@admin.register(MaterialConstructionFamilyCard)
class MaterialConstructionFamilyCardAdmin(SimpleHistoryAdmin):
    list_display = ['family_card', 'material_roof', 'material_wall', 'material_floor', 'number_bedrooms']
    list_filter = ['home_ownership', 'cooking_fuel']
    search_fields = ['family_card__family_card_number']
    history_list_display = ['number_bedrooms', 'ventilation', 'lighting']


# UserProfile admin con gestion de multi-organizacion
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'can_view_all_organizations', 'is_active', 'created_at']
    list_filter = ['role', 'organization', 'can_view_all_organizations', 'is_active']
    search_fields = ['user__username', 'user__email', 'organization__organization_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Usuario', {
            'fields': ('user', 'organization')
        }),
        ('Permisos', {
            'fields': ('role', 'can_view_all_organizations', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """
        Filtrar perfiles segun organizacion del usuario admin.
        Superusuarios ven todos.
        """
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if hasattr(request.user, 'profile'):
            if request.user.profile.can_view_all_organizations:
                return qs
            return qs.filter(organization=request.user.profile.organization)

        return qs.none()

