from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from censoapp.models import Association


# Create your views here.

def home(request):
    return render(request, 'home.html')


def dashboard(request):
    return render(request, 'censo/dashboard.html')


def profile(request):
    return render(request, 'account/profile.html')


class association(ListView):
    model = Association
    title = 'association'
    template_name = 'censo/association.html'
    context_object_name = 'associations'


class createAssociation(CreateView):
    model = Association
    fields = '__all__'
    template_name = 'censo/createAssociation.html'
    success_url = reverse_lazy('association')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(createAssociation, self).form_valid(form)
