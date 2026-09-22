from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Instrumentos
from .forms import InstrumentoForm

# 1. LISTAR / INICIO
def inicio(request):
    # Filtra el catálogo cuando el usuario envía un término de búsqueda.
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