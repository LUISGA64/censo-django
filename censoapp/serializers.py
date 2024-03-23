from rest_framework import serializers
from censoapp.models import Sidewalks, Association, Organizations, DocumentType, CivilState, EducationLevel, Kinship, \
    Occupancy, Gender, SecuritySocial, Eps, Handicap


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




