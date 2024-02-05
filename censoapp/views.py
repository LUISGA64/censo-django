from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from censoapp.models import Association, Person, FamilyCard
from .forms import FormFamilyCard, FormPerson


# Create your views here.
@login_required
def home(request):
    return render(request, 'censo/dashboard.html')


@login_required
def dashboard(request):
    messages.success(request, "Procedimientos registrados")
    return render(request, 'censo/dashboard.html')


@login_required
def profile(request):
    return render(request, 'account/profile.html')


@login_required
def association(request):
    if request.method == 'GET':
        associations = Association.objects.all()
        messages.success(request, "Procedimientos registrados")
        return render(request, 'censo/configuracion/association.html', {'associations': associations})
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
    queryset = Person.objects.select_related('family_card')
    if queryset.exists():
        messages.success(request, "Procedimientos registrados")
    else:
        messages.success(request, "No hay registros")
        return render(request, 'censo/dashboard.html')
    return render(request, 'censo/censo/familyCardIndex.html', {'family_cards': queryset})


# Clase para la ficha familiar y el cabeza de familia
class FamilyCardCreate(SessionWizardView):
    form_list = [FormFamilyCard, FormPerson]
    template_name = 'censo/censo/createFamilyCard.html'

    @transaction.atomic
    def done(self, form_list, **kwargs):
        family_card_data = self.get_cleaned_data_for_step('0')
        person_data = self.get_cleaned_data_for_step('1')
        family_card_count = FamilyCard.objects.count()

        print(family_card_data)
        try:
            with transaction.atomic():
                # filter the data to create the person
                query = Person.objects.filter(identification_person=person_data['identification_person'])
                if query.exists():
                    messages.error(self.request, "Ya existe una persona con esa cédula")
                    return HttpResponse('Ya existe una persona con esa cédula')
                else:
                    family_card = FamilyCard.objects.create(
                        address_home=family_card_data['address_home'],
                        sidewalk_home=family_card_data['sidewalk_home'],
                        latitude=family_card_data['latitude'],
                        longitude=family_card_data['longitude'],
                        zone=family_card_data['zone'],
                        organization_id=family_card_data['organization_id'],
                        family_card_number=family_card_count + 1)

                    persona = Person.objects.create(
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
