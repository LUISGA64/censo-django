from rest_framework import serializers
from censoapp.models import Sidewalks


class SidewalksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sidewalks
        fields = ['sidewalk_name', 'organization_id']

    def create(self, validated_data):
        return Sidewalks.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.sidewalk = validated_data.get('sidewalk', instance.sidewalk)
        instance.organization_id = validated_data.get('organization_id', instance.organization_id)
        instance.save()
        return instance
