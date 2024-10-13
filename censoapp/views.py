from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db import transaction
from django.db.models import Value
from django.db.models.functions.text import Concat

from .choices import handicap
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from censoapp.models import Association, Person, FamilyCard, DocumentType, Gender, SecuritySocial, Eps, Kinship, \
    EducationLevel, CivilState, Occupancy, Sidewalks, Organizations
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
    queryset = (Person.objects.select_related('family_card').select_related('sidewalk_home')
                .filter(family_head=True)
                .values('family_card__family_card_number', 'id', 'first_name_1', 'first_name_2', 'last_name_1',
                        'last_name_2', 'identification_person',
                        'family_card__sidewalk_home__sidewalk_name', 'family_card__zone'))

    # Crear la columna full_name en la consulta
    queryset = queryset.annotate(
        full_name=Concat('first_name_1', Value(' '), 'first_name_2', Value(' '), 'last_name_1', Value(' '),
                         'last_name_2')
    )

    print(queryset)

    # Serializar los datos
    data = list(queryset)

    # Devolver los datos y el total de registros
    response_data = {
        'draw': 1,  # Incrementar esto con cada solicitud de DataTables
        'recordsTotal': len(data),
        'recordsFiltered': len(data),
        'data': data
    }

    return JsonResponse(response_data)


# Clase para la ficha familiar y la cabeza de familia
class FamilyCardPersonCreateView(CreateView):
    model = FamilyCard
    form_class = FormFamilyCard
    template_name = 'censo/censo/createFamilyCard.html'
    success_url = reverse_lazy('familyCardIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['person_form'] = FormPerson(self.request.POST)
        else:
            context['person_form'] = FormPerson()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        person_form = context['person_form']

        identification_person = self.request.POST['identification_person']
        if Person.objects.filter(identification_person=identification_person).exists():
            messages.error(self.request, "Ya existe una persona con esa identificación.")
            return self.form_invalid(form)

        if form.is_valid() and person_form.is_valid():
            try:
                with transaction.atomic():
                    self.object = form.save()
                    person = person_form.save(commit=False)
                    person.family_card = self.object
                    print(person.family_card)
                    person.save()
                    messages.success(self.request, "Familia y persona creadas correctamente.")
                    return super().form_valid(form)
            except Exception as e:
                messages.error(self.request, f"Ocurrió un error: {e}")
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        person_form = context['person_form']
        print(person_form.errors)
        messages.error(self.request, "Hubo errores en el formulario. Por favor, corríjalos e intente nuevamente.")
        return self.render_to_response(self.get_context_data(form=form, person_form=person_form))

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

        print(self.request.POST)
        family_card_number = self.request.POST['family_card_number']

        messages.success(self.request, "Ficha familiar actualizada correctamente")
        return super(UpdateFamily, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Hubo un problema con la actualización de la ficha familiar. "
                                       "Por favor, revisa los campos nuevamente.")
        print("*" * 20 + "Errores" + "*" * 20)
        print(form.errors.as_data())
        print("*" * 40)
        return super(UpdateFamily, self).form_invalid(form)
