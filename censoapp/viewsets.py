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


# ==============================================================================
# API REST - ViewSets Principales con JWT
# ==============================================================================

from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    PersonSerializer, PersonListSerializer,
    FamilyCardSerializer, FamilyCardDetailSerializer,
    GeneratedDocumentSerializer
)
from .models import Person, FamilyCard, GeneratedDocument


class PersonViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Personas via API

    list: Listar todas las personas
    retrieve: Obtener detalle de una persona
    create: Crear nueva persona
    update: Actualizar persona completa
    partial_update: Actualizar persona parcial
    destroy: Eliminar persona (soft delete)
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'document_type', 'family_card', 'family_head', 'state']
    search_fields = ['identification_person', 'first_name_1', 'last_name_1', 'personal_email']
    ordering_fields = ['id', 'first_name_1', 'last_name_1', 'date_birth', 'identification_person']
    ordering = ['-id']

    def get_queryset(self):
        queryset = Person.objects.filter(state=True)

        # Filtrar por organización del usuario
        if hasattr(self.request.user, 'userprofile'):
            if not self.request.user.userprofile.can_view_all_organizations:
                org = self.request.user.userprofile.organization
                if org:
                    queryset = queryset.filter(family_card__organization=org)

        return queryset.select_related(
            'gender', 'document_type', 'education_level',
            'civil_state', 'family_card'
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return PersonListSerializer
        return PersonSerializer

    def perform_destroy(self, instance):
        # Soft delete
        instance.state = False
        instance.save()

    @action(detail=False, methods=['get'])
    def by_family(self, request):
        """Obtener personas de una ficha familiar específica"""
        family_card_id = request.query_params.get('family_card_id')
        if not family_card_id:
            return Response(
                {'error': 'family_card_id es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        personas = self.get_queryset().filter(family_card_id=family_card_id)
        serializer = self.get_serializer(personas, many=True)
        return Response(serializer.data)


class FamilyCardViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Fichas Familiares via API

    list: Listar todas las fichas
    retrieve: Obtener detalle de una ficha con miembros
    create: Crear nueva ficha
    update: Actualizar ficha completa
    partial_update: Actualizar ficha parcial
    destroy: Eliminar ficha (soft delete)
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['organization', 'sidewalk_home', 'state']
    search_fields = ['family_card_number', 'address_home']
    ordering_fields = ['id', 'family_card_number']
    ordering = ['-id']

    def get_queryset(self):
        queryset = FamilyCard.objects.filter(state=True)

        # Filtrar por organización del usuario
        if hasattr(self.request.user, 'userprofile'):
            if not self.request.user.userprofile.can_view_all_organizations:
                org = self.request.user.userprofile.organization
                if org:
                    queryset = queryset.filter(organization=org)

        return queryset.select_related('organization', 'sidewalk_home')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FamilyCardDetailSerializer
        return FamilyCardSerializer

    def perform_destroy(self, instance):
        # Soft delete
        instance.state = False
        instance.save()

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Obtener todos los miembros de una ficha familiar"""
        ficha = self.get_object()
        personas = Person.objects.filter(family_card=ficha, state=True)
        serializer = PersonListSerializer(personas, many=True)
        return Response(serializer.data)


class GeneratedDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Documentos Generados via API

    list: Listar todos los documentos
    retrieve: Obtener detalle de un documento
    create: Crear nuevo documento
    update: Actualizar documento completo
    partial_update: Actualizar documento parcial
    destroy: Eliminar documento
    """
    queryset = GeneratedDocument.objects.all()
    serializer_class = GeneratedDocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['person', 'document_type', 'status']
    search_fields = ['document_number', 'person__identification_person']
    ordering_fields = ['id', 'issue_date', 'expiration_date', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = GeneratedDocument.objects.all()

        # Filtrar por organización del usuario
        if hasattr(self.request.user, 'userprofile'):
            if not self.request.user.userprofile.can_view_all_organizations:
                org = self.request.user.userprofile.organization
                if org:
                    queryset = queryset.filter(organization=org)

        return queryset.select_related('person', 'document_type')

    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Obtener documentos próximos a vencer (30 días)"""
        from datetime import date, timedelta

        end_date = date.today() + timedelta(days=30)
        documentos = self.get_queryset().filter(
            expiration_date__lte=end_date,
            expiration_date__gte=date.today(),
            status='ISSUED'
        )

        serializer = self.get_serializer(documentos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_person(self, request):
        """Obtener documentos de una persona específica"""
        person_id = request.query_params.get('person_id')
        if not person_id:
            return Response(
                {'error': 'person_id es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        documentos = self.get_queryset().filter(person_id=person_id)
        serializer = self.get_serializer(documentos, many=True)
        return Response(serializer.data)
