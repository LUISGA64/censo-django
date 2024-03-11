from rest_framework import viewsets, permissions
from .serializers import SidewalksSerializer, AssociationSerializer, OrganizationSerializer
from .models import Sidewalks, Association, Organizations


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

