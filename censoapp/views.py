from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from formtools.wizard.views import SessionWizardView
from censoapp.models import Association, Person, FamilyCard
from .forms import FormFamilyCard, FormPerson


# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    return render(request, 'censo/dashboard.html')


@login_required
def profile(request):
    return render(request, 'account/profile.html')


@login_required
def association(request):
    associations = Association.objects.all()
    return render(request, 'censo/configuracion/association.html', {'associations': associations})


@login_required
def family_card_index(request):
    family_cards = FamilyCard.objects.all()
    return render(request, 'censo/censo/censoIndex.html', {'family_cards': family_cards, 'form': FormFamilyCard()})


def create_family_card(request):
    form = FormFamilyCard()
    return render(request, 'censo/censo/createFamilyCard.html', {'form': form})


class CreateAssociation(CreateView):
    model = Association
    fields = '__all__'
    template_name = 'censo/createAssociation.html'
    success_url = reverse_lazy('association')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateAssociation, self).form_valid(form)


class FormWizardView(SessionWizardView):
    form_list = [FormFamilyCard, FormPerson]
    template_name = 'censo/censo/createFamilyCard.html'

    @transaction.atomic
    def done(self, form_list, **kwargs):
        family_card_data = self.get_cleaned_data_for_step('0')
        person_data = self.get_cleaned_data_for_step('1')

        try:
            with transaction.atomic():
                family_card = FamilyCard.objects.create(**family_card_data)
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
                    kinship_id=person_data['kinship_id'],
                    handicap=person_data['handicap'],
                    education_level=person_data['education_level'],
                    civil_state=person_data['civil_state'],
                    occupation=person_data['occupation'],
                    family_card=family_card
                )
                return redirect('dashboard')
        except Exception as e:
            # Maneja las excepciones según sea necesario
            print(f"Error durante la creación: {e}")
            return redirect('error_page')  # redirige a una página de error


def create_person(request):
    if request.method == 'POST':
        form = Person(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = Person()
    return render(request, 'censo/createPerson.html', {'form': form})
