from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Instrumentos
from .forms import InstrumentoForm
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# 1. LISTAR / INICIO
def inicio(request):
    # Filtra el catalogo cuando el usuario envia un termino de busqueda.
    busqueda = request.GET.get('q', '').strip()
    instrumentos = Instrumentos.objects.all()

    if busqueda:
        instrumentos = instrumentos.filter(
            Q(nombre__icontains=busqueda)
            | Q(tipo__icontains=busqueda)
            | Q(marca__icontains=busqueda)
        )

    return render(request, 'musicAPP/inicio.html', {
        'instrumentos': instrumentos,
        'busqueda': busqueda,
    })

# 2. CREAR
def agregar_instrumento(request):
    if request.method == 'POST':
        form = InstrumentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = InstrumentoForm()
    return render(request, 'musicAPP/agregar.html', {'form': form})

# 3. EDITAR
def editar_instrumento(request, id):
    instrumento = get_object_or_404(Instrumentos, id=id)
    if request.method == 'POST':
        form = InstrumentoForm(request.POST, instance=instrumento)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = InstrumentoForm(instance=instrumento)
    return render(request, 'musicAPP/editar.html', {'form': form, 'instrumento': instrumento})

# 4. ELIMINAR
def eliminar_instrumento(request, id):
    instrumento = get_object_or_404(Instrumentos, id=id)
    if request.method == 'POST':
        instrumento.delete()
        return redirect('inicio')
    return render(request, 'musicAPP/eliminar.html', {'instrumento': instrumento})

# 5. LOGIN
def login_pagina(request):
    return render(request, 'musicAPP/login.html')


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            token, created = Token.objects.get_or_create(user=usuario)
            return Response({
                'mensaje': 'Inicio de sesión exitoso',
                'usuario': usuario.username,
                'token': token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'mensaje': 'Credenciales inválidas'
            }, status=status.HTTP_401_UNAUTHORIZED)