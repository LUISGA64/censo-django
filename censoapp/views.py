from django.contrib.auth.views import LoginView
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

    def done(self, form_list, **kwargs):
        return render(self.request, 'censo/censo/createFamilyCard.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


def create_person(request):
    if request.method == 'POST':
        form = Person(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = Person()
    return render(request, 'censo/createPerson.html', {'form': form})
