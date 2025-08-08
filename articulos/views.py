from django.shortcuts import render, redirect
from .models import Articulo
from .forms import ArticuloForm

def lista_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'articulos/lista.html', {'articulos': articulos})

def agregar_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm()
    return render(request, 'articulos/formulario.html', {'form': form})

def modificar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm(instance=articulo)
    return render(request, 'articulos/formulario.html', {'form': form, 'titulo': 'Editar artículo'})
    
