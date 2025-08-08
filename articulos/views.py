from django.shortcuts import render, redirect, get_object_or_404
from .models import Articulo
from .forms import ArticuloForm

def login_view(request):
    error = None
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        clave = request.POST.get("clave")

        if usuario == "ADMIN" and clave == "5278":
            request.session["usuario_autenticado"] = True
            return redirect("lista_articulos")
        else:
            error = "Usuario o clave incorrectos"

    return render(request, "articulos/login.html", {"error": error})


def logout_view(request):
    # Cierra sesión
    request.session.flush()
    return redirect("login")


def lista_articulos(request):
    # Protegemos la vista
    if not request.session.get("usuario_autenticado"):
        return redirect("login")

    articulos = Articulo.objects.all()
    return render(request, 'articulos/lista.html', {'articulos': articulos})


def agregar_articulo(request):
    if not request.session.get("usuario_autenticado"):
        return redirect("login")

    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm()
    return render(request, 'articulos/formulario.html', {'form': form, 'titulo': 'Agregar artículo'})


def modificar_articulo(request, pk):
    if not request.session.get("usuario_autenticado"):
        return redirect("login")

    articulo = get_object_or_404(Articulo, pk=pk)
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm(instance=articulo)
    return render(request, 'articulos/formulario.html', {'form': form, 'titulo': 'Editar artículo'})
    
    
