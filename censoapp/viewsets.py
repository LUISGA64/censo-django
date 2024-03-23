from rest_framework import viewsets, permissions
from .serializers import SidewalksSerializer, AssociationSerializer, OrganizationSerializer, DocumentTypeSerializer, \
    CivilStateSerializer, EducationLevelSerializer, EpsSerializer, KinshipSerializer, OccupancySerializer, \
    GenderSerializer, SecuritySocialSerializer, HandicapSerializer
from .models import Sidewalks, Association, Organizations, DocumentType, CivilState, EducationLevel, Eps, Kinship, \
    Occupancy, Gender, SecuritySocial, Handicap


class SidewalksViewSet(viewsets.ModelViewSet):
    queryset = Sidewalks.objects.all()
    serializer_class = SidewalksSerializer

    def get_queryset(self):
        queryset = Sidewalks.objects.all()
        organization_id = self.request.query_params.get('organization_id', None)
        if organization_id is not None:
            queryset = queryset.filter(organization_id=organization_id)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}


class AssociationViewSet(viewsets.ModelViewSet):
    queryset = Association.objects.all()
    serializer_class = AssociationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationSerializer


class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer


class CivilStateViewSet(viewsets.ModelViewSet):
    queryset = CivilState.objects.all()
    serializer_class = CivilStateSerializer


class EducationLevelViewSet(viewsets.ModelViewSet):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer


class EpsViewSet(viewsets.ModelViewSet):
    queryset = Eps.objects.all()
    serializer_class = EpsSerializer


class KinshipViewSet(viewsets.ModelViewSet):
    queryset = Kinship.objects.all()
    serializer_class = KinshipSerializer


class OccupancyViewSet(viewsets.ModelViewSet):
    queryset = Occupancy.objects.all()
    serializer_class = OccupancySerializer


class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class SecurityViewSet(viewsets.ViewSet):
    queryset = SecuritySocial.objects.all()
    serializer_class = SecuritySocialSerializer


class HandicapViewSet(viewsets.ViewSet):
    queryset = Handicap.objects.all()
    serializer_class = HandicapSerializer
