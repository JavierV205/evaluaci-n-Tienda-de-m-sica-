from django.shortcuts import render,redirect
from .models import Instrumentos


# Create your views here.
def inicio(request):
    instrumentos= Instrumentos.objects.all()

    return render(request, 'musicAPP/inicio.html', {'instrumentos': instrumentos})