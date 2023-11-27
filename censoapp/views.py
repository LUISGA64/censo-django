from django.shortcuts import render

# Create your views here.
def index(request):
    data = request.session['moticas'] = 'hola'
    return render(request, 'censo/base_site.html')