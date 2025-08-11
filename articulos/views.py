from django.shortcuts import render, redirect, get_object_or_404
from .models import Articulo
from .forms import ArticuloForm

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').upper()
        password = request.POST.get('password', '')
        if username == 'ADMIN' and password == '5278':
            request.session['usuario_autenticado'] = True  # Marcamos sesión activa
            return redirect('lista_articulos')
        else:
            error = 'Usuario o contraseña incorrectos.'
    return render(request, 'articulos/login.html', {'error': error})

def logout_view(request):
    request.session.flush()  # Limpiamos la sesión
    return redirect('login')

def menu_principal(request):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')
    return render(request, 'articulos/menu.html')

def lista_articulos(request):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')
    articulos = Articulo.objects.all()  # Traemos todos los artículos
    return render(request, 'articulos/lista.html', {'articulos': articulos})

def agregar_articulo(request):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')

    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm()
    return render(request, 'articulos/formulario.html', {
        'form': form,
        'titulo': 'Agregar artículo'})

def modificar_articulo(request, pk):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')

    articulo = get_object_or_404(Articulo, pk=pk)
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('lista_articulos')
    else:
        form = ArticuloForm(instance=articulo)
    return render(request, 'articulos/formulario.html', {'form': form, 'titulo': 'Editar artículo'})

def eliminar_articulo(request, pk):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')

    articulo = get_object_or_404(Articulo, pk=pk)
    articulo.delete()
    return redirect('lista_articulos')
