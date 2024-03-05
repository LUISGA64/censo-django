from datetime import datetime
from json import dumps

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db import transaction
from .choices import handicap
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from censoapp.models import Association, Person, FamilyCard, DocumentType, Gender, SecuritySocial, Eps, Kinship, \
    EducationLevel, CivilState, Occupancy
from .forms import FormFamilyCard, FormPerson


# Create your views here.
@login_required
def home(request):
    return render(request, 'censo/dashboard.html', {'segment': 'dashboard'})


@login_required
def dashboard(request):
    messages.info(request, "Mensaje de prueba")
    return render(request, 'censo/dashboard.html')


@login_required
def profile(request):
    return render(request, 'account/profile.html')


@login_required
def association(request):
    if request.method == 'GET':
        associations = Association.objects.all()
        context = {'segment': 'association'}
        messages.success(request, "Procedimientos registrados")
        return render(request, 'censo/configuracion/association.html',
                      {'associations': associations, 'segment': 'association'})
    else:
        messages.error(request, "No se pudo cargar la página")
        return HttpResponse('No se pudo cargar la página')


class CreateAssociation(CreateView):
    model = Association
    fields = '__all__'
    template_name = 'censo/createAssociation.html'
    success_url = reverse_lazy('association')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateAssociation, self).form_valid(form)


def family_card_index(request):
    queryset = Person.objects.select_related('family_card').filter(family_head=True)
    return render(request, 'censo/censo/familyCardIndex.html',
                  {'family_cards': queryset, 'segment': 'family_card'})


def get_family_cards(request):
    queryset = Person.objects.select_related('family_card').filter(family_head=True)
    data = serialize('json', queryset, fields=('id', 'first_name_1', 'first_name_2', 'last_name_1',
                                               'last_name_2', 'identification_person',
                                               'family_card__family_card_number',
                                               'family_card__sidewalk_home', 'family_card__zone'))
    return JsonResponse(data, safe=False)



# Clase para la ficha familiar y el cabeza

class FamilyCardCreate(SessionWizardView):
    form_list = [FormFamilyCard, FormPerson]
    template_name = 'censo/censo/createFamilyCard.html'

    @transaction.atomic
    def done(self, form_list, **kwargs):
        family_card_data = self.get_cleaned_data_for_step('0')
        person_data = self.get_cleaned_data_for_step('1')
        family_card_count = FamilyCard.objects.count()

        try:
            with transaction.atomic():
                # filter the data to create the person
                query = Person.objects.filter(identification_person=person_data['identification_person'])
                if query.exists():
                    messages.error(self.request, "Ya existe una persona con esa cédula")

                else:
                    family_card = FamilyCard.objects.create(
                        address_home=family_card_data['address_home'],
                        sidewalk_home=family_card_data['sidewalk_home'],
                        latitude=family_card_data['latitude'],
                        longitude=family_card_data['longitude'],
                        zone=family_card_data['zone'],
                        organization_id=family_card_data['organization_id'],
                        family_card_number=family_card_count + 1)

                    Person.objects.create(
                        first_name_1=person_data['first_name_1'],
                        first_name_2=person_data['first_name_2'],
                        last_name_1=person_data['last_name_1'],
                        last_name_2=person_data['last_name_2'],
                        identification_person=person_data['identification_person'],
                        document_type=person_data['document_type'],
                        cell_phone=person_data['cell_phone'],
                        personal_email=person_data['personal_email'],
                        gender_id=person_data['gender_id'],
                        date_birth=person_data['date_birth'],
                        social_insurance=person_data['social_insurance'],
                        eps=person_data['eps'],
                        kinship_id=person_data['kinship_id'],
                        handicap=person_data['handicap'],
                        education_level=person_data['education_level'],
                        civil_state=person_data['civil_state'],
                        occupation=person_data['occupation'],
                        family_card=family_card,
                        family_head=True
                    )
                    messages.success(self.request, "Ficha familiar creada correctamente")
                    return redirect('dashboard')
        except Exception as e:
            # Maneja las excepciones según sea necesario
            print(f"Error durante la creación: {e}")
            messages.error(self.request, "No se pudo crear la ficha familiar")
            return redirect('error_page')  # redirige a una página de error


@login_required
def crear_persona(request, pk):
    familia = pk
    if request.method == 'POST':
        query = Person.objects.filter(identification_person=request.POST['identification_person'])
        if query.exists():
            messages.error(request, "Ya existe una persona con esa identificación")
            return redirect('createPerson', familia)
        else:
            first_name_1 = request.POST['first_name_1']
            first_name_2 = request.POST['first_name_2']
            last_name_1 = request.POST['last_name_1']
            last_name_2 = request.POST['last_name_2']
            identification_person = request.POST['identification_person']
            document_type = int(request.POST['document_type'])
            cell_phone = request.POST['cell_phone']
            personal_email = request.POST['personal_email']
            gender_id = request.POST['gender_id']
            date_birth = datetime.strptime(request.POST['date_birth'], '%Y-%m-%d').date()
            social_insurance = request.POST['social_insurance']
            eps = request.POST['eps']
            kinship_id = request.POST['kinship_id']
            handicap = request.POST['handicap']
            education_level = request.POST['education_level']
            civil_state = request.POST['civil_state']
            occupation = request.POST['occupation']
            # family_card = familia
            Person.objects.create(
                first_name_1=first_name_1,
                first_name_2=first_name_2,
                last_name_1=last_name_1,
                last_name_2=last_name_2,
                identification_person=identification_person,
                document_type=DocumentType.objects.get(pk=document_type),
                cell_phone=cell_phone,
                personal_email=personal_email,
                gender_id=Gender.objects.get(pk=gender_id),
                date_birth=date_birth,
                social_insurance=SecuritySocial.objects.get(pk=social_insurance),
                eps=Eps.objects.get(pk=eps),
                kinship_id=Kinship.objects.get(pk=kinship_id),
                handicap=handicap,
                education_level=EducationLevel.objects.get(pk=education_level),
                civil_state=CivilState.objects.get(pk=civil_state),
                occupation=Occupancy.objects.get(pk=occupation),
                family_card=FamilyCard.objects.get(pk=familia),
                family_head=False)
            messages.success(request, "Persona creada correctamente, Registre otra persona si lo desea.")
            return redirect('createPerson', familia)

    else:
        form = FormPerson()
    return render(request, 'censo/censo/createPerson.html',
                  {'form': form, 'familia': familia, 'segment': 'family_card'})


def detalle_ficha(request, pk):
    familia = Person.objects.select_related('family_card').select_related('kinship_id').filter(family_card=pk)
    return render(request, 'censo/censo/detail_family_card.html',
                  {'familia': familia, 'segment': 'family_card'})


# def editar_ficha(request, pk):
#     familia = FamilyCard.objects.filter(id=pk)
#     print(familia)
#     return render(request, 'censo/censo/edit-family-card.html',
#                   {'segment': 'family_card', 'familia': familia})

class UpdateFamily(UpdateView):
    model = FamilyCard
    fields = '__all__'
    template_name = 'censo/censo/edit-family-card.html'
    success_url = reverse_lazy('familyCardIndex')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Ficha familiar actualizada correctamente")
        return super(UpdateFamily, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Hubo un problema con la actualización de la ficha familiar. "
                                       "Por favor, revisa los campos nuevamente.")
        return super(UpdateFamily, self).form_invalid(form)