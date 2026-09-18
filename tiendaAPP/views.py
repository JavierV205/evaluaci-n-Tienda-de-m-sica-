from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Bienvenido a la tienda de música")