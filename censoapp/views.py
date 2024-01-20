from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from censoapp.models import Association, Person
from censoapp.forms import FormFamilyCard


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


def censo_index(request):
    return render(request, 'censo/censo/censoIndex.html')


def registrar_censo(request):
    if request.method == 'POST':
        form = FormFamilyCard(request.POST)
        if form.is_valid():
            form.save()
            return redirect('censo_index')
    else:
        form = FormFamilyCard()
    return render(request, 'censo/censo/registrarCenso.html')


class CreateAssociation(CreateView):
    model = Association
    fields = '__all__'
    template_name = 'censo/createAssociation.html'
    success_url = reverse_lazy('association')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateAssociation, self).form_valid(form)


def create_person(request):
    if request.method == 'POST':
        form = Person(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = Person()
    return render(request, 'censo/createPerson.html', {'form': form})

