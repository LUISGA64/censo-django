from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


# Create your views here.

class LoginView(LoginView):
    template_name = 'index.html'
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


def home(request):
    return render(request, 'registration/login.html')


@login_required
def association(request):
    return render(request, 'censo/base_site.html')