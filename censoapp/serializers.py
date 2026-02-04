from rest_framework import serializers
from censoapp.models import Sidewalks, Association, Organizations, DocumentType, CivilState, EducationLevel, Kinship, \
    Occupancy, Gender, SecuritySocial, Eps, Handicap, Person, FamilyCard, GeneratedDocument


class SidewalksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sidewalks
        fields = ['id', 'sidewalk_name', 'organization_id']

    def create(self, validated_data):
        return Sidewalks.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.sidewalk = validated_data.get('sidewalk', instance.sidewalk)
    #     instance.organization_id = validated_data.get('organization_id', instance.organization_id)
    #     instance.save()
    #     return instance


class AssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizations
        fields = '__all__'


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'


class CivilStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CivilState
        fields = '__all__'


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = '__all__'


class EpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eps
        fields = '__all__'


class KinshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kinship
        fields = '__all__'


class OccupancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupancy
        fields = '__all__'


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model: Gender
        fields = '__all__'


class SecuritySocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySocial
        fields = '__all__'


class HandicapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Handicap
        fields = '__all__'


# =============================================================================
# API REST - Serializers Principales
# ==============================================================================

class PersonSerializer(serializers.ModelSerializer):
    """Serializer para Person con información completa"""
    gender_name = serializers.CharField(source='gender.gender', read_only=True)
    document_type_name = serializers.CharField(source='document_type.document_type', read_only=True)
    education_level_name = serializers.CharField(source='education_level.education_level', read_only=True)
    civil_state_name = serializers.CharField(source='civil_state.state_civil', read_only=True)
    family_card_number = serializers.CharField(source='family_card.family_card_number', read_only=True)
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = [
            'id', 'identification_person', 'first_name_1', 'first_name_2',
            'last_name_1', 'last_name_2', 'full_name', 'date_birth', 'age',
            'gender', 'gender_name', 'document_type', 'document_type_name',
            'education_level', 'education_level_name', 'civil_state', 'civil_state_name',
            'family_card', 'family_card_number', 'family_head',
            'email', 'phone_number', 'occupation',
            'state', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        return obj.full_name

    def get_age(self, obj):
        if obj.date_birth:
            from datetime import date
            today = date.today()
            return today.year - obj.date_birth.year - ((today.month, today.day) < (obj.date_birth.month, obj.date_birth.day))
        return None


class PersonListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados"""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['id', 'identification_person', 'full_name', 'date_birth', 'phone_number']

    def get_full_name(self, obj):
        return obj.full_name


class FamilyCardSerializer(serializers.ModelSerializer):
    """Serializer para FamilyCard con información completa"""
    organization_name = serializers.CharField(source='organization.acronym', read_only=True)
    sidewalk_name = serializers.CharField(source='sidewalk_home.sidewalk_name', read_only=True)
    members_count = serializers.SerializerMethodField()
    family_head = serializers.SerializerMethodField()

    class Meta:
        model = FamilyCard
        fields = [
            'id', 'family_card_number', 'organization', 'organization_name',
            'sidewalk_home', 'sidewalk_name', 'address_home',
            'latitude', 'longitude', 'members_count', 'family_head',
            'state', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_members_count(self, obj):
        return Person.objects.filter(family_card=obj, state=True).count()

    def get_family_head(self, obj):
        head = Person.objects.filter(family_card=obj, family_head=True, state=True).first()
        if head:
            return {
                'id': head.id,
                'name': head.full_name,
                'identification': head.identification_person
            }
        return None


class FamilyCardDetailSerializer(FamilyCardSerializer):
    """Serializer detallado con miembros de la familia"""
    members = PersonListSerializer(source='person_set', many=True, read_only=True)

    class Meta(FamilyCardSerializer.Meta):
        fields = FamilyCardSerializer.Meta.fields + ['members']


class GeneratedDocumentSerializer(serializers.ModelSerializer):
    """Serializer para Documentos Generados"""
    person_name = serializers.CharField(source='person.full_name', read_only=True)
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = GeneratedDocument
        fields = [
            'id', 'document_number', 'person', 'person_name',
            'document_type', 'document_type_name', 'issue_date',
            'expiration_date', 'is_expired', 'status',
            'qr_code', 'created_at'
        ]
        read_only_fields = ['id', 'document_number', 'qr_code', 'created_at']

    def get_is_expired(self, obj):
        if obj.expiration_date:
            from datetime import date
            return obj.expiration_date < date.today()
        return False
