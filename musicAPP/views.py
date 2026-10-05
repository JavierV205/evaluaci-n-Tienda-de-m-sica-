from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Instrumentos
from .forms import InstrumentoForm
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# 1. LISTAR / INICIO
@login_required
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
@login_required
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
@login_required
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
@login_required
def eliminar_instrumento(request, id):
    instrumento = get_object_or_404(Instrumentos, id=id)
    if request.method == 'POST':
        instrumento.delete()
        return redirect('inicio')
    return render(request, 'musicAPP/eliminar.html', {'instrumento': instrumento})

# 5. LOGIN
def login_pagina(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    return render(request, 'musicAPP/login.html')


@login_required
@require_POST
def cerrar_sesion(request):
    Token.objects.filter(user=request.user).delete()
    logout(request)
    return redirect('login_pagina')


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not isinstance(username, str) or not username.strip():
            return Response(
                {'mensaje': 'Debes ingresar un nombre de usuario.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(password, str) or not password:
            return Response(
                {'mensaje': 'Debes ingresar una contraseña.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # validacion de caracteres
        if len(username) > 30:
            return Response(
                {'mensaje': 'El nombre de usuario no debe exceder los 30 caracteres.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(password) > 20:
            return Response(
                {'mensaje': 'La contraseña no puede exceder los 20 caracteres.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request._request, usuario)
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