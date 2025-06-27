import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError
from django.db.models import Value, Q, F, ExpressionWrapper, fields, Count
from django.db.models.functions.text import Concat
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.forms import inlineformset_factory
from censoapp.models import Association, Person, FamilyCard
from .forms import FormFamilyCard, FormPerson

logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def home(request):
    cantidad = Person.objects.values_list('gender__gender').annotate(cantidad=Count('id'))

    print("Cantidad de personas por género:", cantidad)

    # Crear un diccionario a partir de los resultados de la consulta
    cantidad_dict = {}
    for item in cantidad:
        cantidad_dict[item[0]] = item[1]

    context = {'segment': 'dashboard', 'cantidad_genero': cantidad_dict}
    return render(request, 'censo/dashboard.html', context)


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
    return render(request, 'censo/censo/familyCardIndex.html',
                  {'segment': 'family_card'})


# Función para obtener las fichas familiares en formato JSON para DataTables
def get_family_cards(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    queryset = (Person.objects.select_related('family_card', 'sidewalk_home')
                .filter(family_head=True)
                .values('family_card__family_card_number', 'family_card_id', 'first_name_1', 'first_name_2', 'last_name_1',
                        'last_name_2', 'identification_person', 'document_type__code_document_type',
                        'family_card__sidewalk_home__sidewalk_name', 'family_card__zone')).order_by('id')

    # Crear la columna full_name en la consulta
    queryset = queryset.annotate(
        full_name=Concat('first_name_1', Value(' '), 'first_name_2', Value(' '), 'last_name_1', Value(' '),
                         'last_name_2'),
        person_count=Count('family_card__person'),
        persona_count_gender=Count('family_card__person__gender'),
    )



    # Filtrar por el valor de búsqueda
    if search_value:
        queryset = queryset.filter(
            Q(full_name__icontains=search_value) |
            Q(identification_person__icontains=search_value) |
            Q(family_card__family_card_number__icontains=search_value) |
            Q(family_card__sidewalk_home__sidewalk_name__icontains=search_value) |
            Q(family_card__zone__icontains=search_value)
        ).order_by('id')

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

        # Verificar si el número de identificación ya existe
        if 'identification_person' in request.POST:
            identification_person = request.POST['identification_person']
            if Person.objects.filter(identification_person=identification_person).exists():
                messages.error(request, "Ya existe una persona con esa identificación.")

            family_card_form_is_valid = family_card_form.is_valid()
            print(f"Family Card Form Valid: {family_card_form_is_valid}")
            person_form_is_valid = person_form.is_valid()
            print(f"Person Form Valid: {person_form_is_valid}")


        if family_card_form.is_valid() and person_form.is_valid():
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
                messages.error(request, f"Hubo un problema al crear la ficha familiar: {str(e)}")
                print(f"Error inesperado: {e}")
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
                # logger.warning(f"Errores del formulario: {person_form.errors}")
    else:
        person_form = FormPerson()

    return render(request, 'censo/persona/createPerson.html', {
        'person_form': person_form,
        'familia': familia,
        'segment': 'family_card'
    })

# Muestra el detalle de la ficha familiar
@login_required
def detalle_ficha(request, pk):

    familia = (Person.objects.
               select_related('family_card', 'kinship', 'document_type', 'sidewalk')
               .filter(family_card_id=pk)
               .values('id', 'first_name_1', 'first_name_2', 'last_name_1', 'last_name_2', 'date_birth',
                       'identification_person', 'document_type__code_document_type', 'kinship__description_kinship',
                       'family_card__family_card_number', 'family_card__sidewalk_home__sidewalk_name', 'family_head',
                       'family_card__zone', 'family_card__address_home')
               .annotate(age=ExpressionWrapper(now().year - F('date_birth__year'), output_field=fields.IntegerField()))
               )

    return render(request, 'censo/censo/detail_family_card.html',
                  {'familia': familia, 'segment': 'family_card', })


class UpdateFamily(LoginRequiredMixin, UpdateView):
    model = FamilyCard
    fields = ['address_home', 'sidewalk_home', 'latitude', 'longitude', 'zone', 'organization']
    template_name = 'censo/censo/edit-family-card.html'
    success_url = reverse_lazy('familyCardIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        PersonFormSet = inlineformset_factory(
            FamilyCard, Person, form=FormPerson, extra=0, can_delete=True
        )
        if self.request.POST:
            context['person_formset'] = PersonFormSet(self.request.POST, instance=self.object)
        else:
            context['person_formset'] = PersonFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        person_formset = context['person_formset']
        if person_formset.is_valid():
            self.object = form.save()
            person_formset.instance = self.object
            person_formset.save()
            messages.success(self.request, "Ficha familiar y personas actualizadas correctamente")
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class DetailPersona(DetailView):
    model = Person
    template_name = 'censo/persona/detail_person.html'
    context_object_name = 'persona'

    def get_queryset(self):
        return (Person.objects
                .select_related('document_type', 'gender','education_level', 'civil_state', 'occupation',
                                'security_social', 'eps', 'kinship', 'family_card', 'handicap')
                .filter(id=self.kwargs['pk'], state=True)
                .values('id', 'first_name_1', 'first_name_2', 'last_name_1', 'last_name_2',
                        'identification_person', 'document_type__document_type', 'date_birth', 'gender__gender',
                        'document_type__code_document_type', 'cell_phone', 'personal_email', 'handicap__handicap',
                        'education_level__education_level', 'civil_state__state_civil', 'kinship__description_kinship',
                        'occupation__description_occupancy', 'eps__name_eps', 'social_insurance__affiliation',
                        'family_card__sidewalk_home__sidewalk_name', 'family_head', 'family_card__zone', 'family_card__address_home'))


# Lista las personas en formato JSON para DataTables

@login_required
def listar_personas(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 7))
    search_value = request.GET.get('search[value]', '')
    order_column = request.GET.get('order[0][column]', '0')
    order_dir = request.GET.get('order[0][dir]', 'asc')

    order_columns = [
        'first_name_1',
        'identification_person',
        'document_type__document_type',
        'date_birth',
        'gender__gender',
        'document_type__code_document_type',
        'family_head',
        'family_card__family_card_number',
        'family_card'
    ]

    order_by = order_columns[int(order_column)]
    if order_dir == 'desc':
        order_by = f'-{order_by}'

    personas = (Person.objects
                .select_related('document_type', 'gender')
                .values('id', 'first_name_1', 'first_name_2', 'last_name_1', 'last_name_2',
                        'identification_person', 'document_type__document_type', 'date_birth', 'family_card',
                        'document_type__code_document_type', 'family_head', 'family_card__family_card_number')
                .annotate(gender=F('gender__gender'),
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


# Vista para mostrar la lista de personas en la plantilla HTML.
def view_persons(request):
    return render(request, 'censo/persona/listado_personas.html', {'segment': 'personas'})


# Vista para editar una persona
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


def person_by_gender(request):
    # Contar las personas por género
    cantidad = Person.objects.values('gender__gender')

    return JsonResponse({'cantidad': cantidad})

