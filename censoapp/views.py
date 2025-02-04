import logging
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db import transaction, IntegrityError
from django.db.models import Value, Q, F, ExpressionWrapper, fields
from django.db.models.functions.text import Concat
from django.utils.timezone import now
from django.views import View
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

logger = logging.getLogger(__name__)

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


# Función para obtener las fichas familiares en formato JSON para DataTables
def get_family_cards(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    queryset = (Person.objects.select_related('family_card', 'sidewalk_home')
                .filter(family_head=True)
                .values('family_card__family_card_number', 'family_card_id', 'first_name_1', 'first_name_2', 'last_name_1',
                        'last_name_2', 'identification_person',
                        'family_card__sidewalk_home__sidewalk_name', 'family_card__zone'))

    # Crear la columna full_name en la consulta
    queryset = queryset.annotate(
        full_name=Concat('first_name_1', Value(' '), 'first_name_2', Value(' '), 'last_name_1', Value(' '),
                         'last_name_2')
    )

    # Filtrar por el valor de búsqueda
    if search_value:
        queryset = queryset.filter(
            Q(full_name__icontains=search_value) |
            Q(identification_person__icontains=search_value) |
            Q(family_card__family_card_number__icontains=search_value) |
            Q(family_card__sidewalk_home__sidewalk_name__icontains=search_value) |
            Q(family_card__zone__icontains=search_value)
        )

    # Paginación
    paginator = Paginator(queryset, length)
    page = paginator.get_page(start // length + 1)


    # Serializar los datos
    data = list(page.object_list)

    # Devolver los datos y el total de registros
    response_data = {
        'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'data': data
    }
    return JsonResponse(response_data)

# Función para crear una ficha familiar y una persona en la misma vista (Wizard)
@login_required
def create_family_card(request):
    if request.method == 'POST':
        family_card_form = FormFamilyCard(request.POST)
        person_form = FormPerson(request.POST)

        if family_card_form.is_valid() and person_form.is_valid():
            identification_person = person_form.cleaned_data['identification_person']

            if Person.objects.filter(identification_person=identification_person).exists():
                messages.error(request, "Ya existe una persona con esa identificación.")
                return render(request, 'censo/censo/createFamilyCard.html', {
                    'family_card_form': family_card_form,
                    'person_form': person_form,
                    'segment': 'family_card'
                })

            try:
                with transaction.atomic():

                    # Crear instancia de FamilyCard
                    family_card = family_card_form.save(commit=False)
                    family_card.family_card_number = FamilyCard.objects.count() + 1
                    family_card.save()

                    # Crear instancia de Person
                    person = person_form.save(commit=False)
                    person.family_card = family_card
                    person.family_head = True
                    person.save()

                    messages.success(request, "Ficha familiar creada correctamente")
                    return redirect('createPerson', pk=family_card.pk)
            except IntegrityError as e:
                logger.error(f"Error de base de datos: {e}")
                messages.error(request, "Hubo un problema al crear la ficha familiar. Por favor, revise los campos nuevamente.")
            except Exception as e:
                logger.error(f"Error inesperado: {e}")
                messages.error(request, "Ocurrió un error inesperado. Por favor, intente nuevamente.")
        else:
            messages.warning(request, "Hubo un problema al crear la ficha familiar. Por favor, revise los campos nuevamente.")
            logger.warning(f"Errores del formulario: {family_card_form.errors}, {person_form.errors}")
    else:
        family_card_form = FormFamilyCard()
        person_form = FormPerson()

    return render(request, 'censo/censo/createFamilyCard.html', {
        'family_card_form': family_card_form,
        'person_form': person_form,
        'segment': 'family_card'
    })


@login_required
def crear_persona(request, pk):
    familia = FamilyCard.objects.get(pk=pk)
    if request.method == 'POST':
        query = Person.objects.filter(identification_person=request.POST['identification_person'])
        person_form = FormPerson(request.POST)
        if person_form.is_valid():
            if query.exists():
                messages.error(request, "Ya existe una persona con esa identificación")
                return render(request, 'censo/censo/../templates/censo/persona/createPerson.html', {
                    'form': person_form,
                    'familia': familia,
                    'segment': 'family_card'
                })

            try:
                with transaction.atomic():
                    person = person_form.save(commit=False)
                    person.family_card = familia
                    person.state = True
                    person.save()
                    messages.success(request, "Persona creada correctamente, Registre otra persona si lo desea.")

                    # Redireccionar a la creación de otra persona o a la lista de fichas familiares
                    if 'add_another' in request.POST:
                        return redirect('createPerson', pk=familia.pk)
                    else:
                        return redirect('familyCardIndex')
            except IntegrityError as e:
                messages.error(request, "Hubo un problema al crear la persona. Por favor, revise los campos nuevamente.")

            else:
                messages.warning(request, "Hubo un problema al crear la persona. Por favor, revise los campos nuevamente.")
                logger.warning(f"Errores del formulario: {person_form.errors}")
    else:
        person_form = FormPerson()

    return render(request, 'censo/persona/createPerson.html', {
        'person_form': person_form,
        'familia': familia,
        'segment': 'family_card'
    })

# Muestra el detalle de la ficha familiar
def detalle_ficha(request, pk):

    print(pk)

    familia = (Person.objects.
               select_related('family_card', 'kinship')
               .filter(family_card_id=pk))

    print(familia)

    return render(request, 'censo/censo/detail_family_card.html',
                  {'familia': familia, 'segment': 'family_card', })


class UpdateFamily(UpdateView):
    model = FamilyCard
    fields = ['address_home', 'sidewalk_home', 'latitude', 'longitude', 'zone', 'organization']
    template_name = 'censo/censo/edit-family-card.html'
    success_url = reverse_lazy('familyCardIndex')

    def form_valid(self, form):
        form.instance.user = self.request.user

        messages.success(self.request, "Ficha familiar actualizada correctamente")
        return super(UpdateFamily, self).form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Errores del formulario: {form.errors}")
        messages.warning(self.request, "Hubo un problema con la actualización de la ficha familiar. "
                                       "Por favor, revisa los campos nuevamente.")

        return super(UpdateFamily, self).form_invalid(form)

def listar_personas(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    order_column = request.GET.get('order[0][column]', '0')
    order_dir = request.GET.get('order[0][dir]', 'asc')

    order_columns = [
        'first_name_1',
        'identification_person',
        'document_type__document_type',
        'date_birth',
        'date_birth',
        'gender__gender'
    ]

    order_by = order_columns[int(order_column)]
    if order_dir == 'desc':
        order_by = f'-{order_by}'

    personas = (Person.objects
                .select_related('document_type', 'gender')
                .values('id', 'first_name_1', 'first_name_2', 'last_name_1', 'last_name_2',
                        'identification_person', 'document_type__document_type', 'date_birth')
                .annotate(gender=F('gender__gender_code'),
                          age=ExpressionWrapper(now().year -F('date_birth__year'), output_field=fields.IntegerField()))
                .filter(state=True))

    if search_value:
        personas = personas.filter(
            Q(first_name_1__icontains=search_value) |
            Q(first_name_2__icontains=search_value) |
            Q(last_name_1__icontains=search_value) |
            Q(last_name_2__icontains=search_value) |
            Q(identification_person__icontains=search_value)
        )

    personas = personas.order_by(order_by)

    paginator = Paginator(personas, length)
    page = paginator.get_page(start // length + 1)

    data = list(page.object_list)

    response_data = {
        'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'data': data
    }

    return JsonResponse(response_data)


def view_persons(request):
    return render(request, 'censo/persona/listado_personas.html', {'segment': 'personas'})


class UpdatePerson(UpdateView):
    model = Person
    fields = ['first_name_1', 'first_name_2', 'last_name_1', 'last_name_2', 'document_type', 'identification_person',
              'date_birth', 'cell_phone', 'personal_email', 'gender', 'kinship', 'education_level', 'civil_state',
              'occupation', 'social_insurance', 'eps', 'handicap', 'state', 'family_head']
    template_name = 'censo/persona/edit_person.html'
    success_url = reverse_lazy('personas')

    def form_valid(self, person_form):
        person_form.instance.user = self.request.user

        messages.success(self.request, "Persona actualizada correctamente")
        return super(UpdatePerson, self).form_valid(person_form)

    def form_invalid(self, form):
        logger.warning(f"Errores del formulario: {form.errors}")
        messages.warning(self.request, "Hubo un problema con la actualización de la persona. "
                                       "Por favor, revisa los campos nuevamente.")

        return super(UpdatePerson, self).form_invalid(form)
