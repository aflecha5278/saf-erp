from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Articulo, ParametroSistema
from .forms import ArticuloForm, LoginForm, ParametroSistemaForm
from django.contrib import messages

def login_view(request):
    error = None
    mensaje_beta = "🔒 Modo Beta: Solo los administradores pueden ingresar."

    if request.method == 'POST':
        username = request.POST.get('username', '').strip().upper()
        password = request.POST.get('password', '').strip()
        form = LoginForm(request.POST)

        if username == 'ADMIN' and password == '5278':
            request.session['usuario_autenticado'] = True  # Marcamos sesión activa
            return redirect('menu_principal')
        else:
            error = 'Usuario o contraseña incorrectos.'
    else:
        form = LoginForm()

    return render(request, 'articulos/login.html', {
        'form': form,
        'error': error,
        'mensaje_beta': mensaje_beta
    })

def logout_view(request):
    request.session.flush()  # Limpiamos la sesión
    return redirect('login')

def menu_principal(request):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')
    return render(request, 'articulos/menu.html')    
    
def lista_articulos(request):
    articulos = Articulo.objects.all().order_by('codart')

    q = request.GET.get('q', '')
    if q:
        articulos = articulos.filter(
            Q(codart__icontains=q) |
            Q(descrip__icontains=q)
        )
    return render(request, 'articulos/lista.html', {'articulos': articulos})

def agregar_articulo(request):
    
    codart_auto = ParametroSistema.objects.filter(clave='CODART_AUTO').first()
    codart_auto_activo = ParametroSistema.objects.filter(clave='CODART_AUTO', valor='S').exists()
    codigo_sugerido = obtener_codigo_sugerido() if codart_auto_activo else ''
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, codart_auto_activo=codart_auto_activo)
        if form.is_valid():
            print("✅ Formulario válido → guardando...")
            articulo = Articulo()
            if codart_auto_activo:
                articulo.codart = codigo_sugerido
            else:
                articulo.codart = form.cleaned_data['codart']
            articulo.descrip = form.cleaned_data['descrip']
            articulo.precosto = round(float(form.cleaned_data['precosto']), 2)
            articulo.margen = round(float(form.cleaned_data['margen']), 2)
            articulo.prefinal = round(float(form.cleaned_data['prefinal'] or 0), 2) if form.cleaned_data['prefinal'] else None
            articulo.modo_calculo = form.cleaned_data['modo_calculo']
            articulo.ncodalic = form.cleaned_data['ncodalic']
            if form.cleaned_data['marca']:
                articulo.marca_id = form.cleaned_data['marca'].id
            if form.cleaned_data['rubro']:
                articulo.rubro_id = form.cleaned_data['rubro'].id
            if form.cleaned_data['subrubro']:
                articulo.subrubro_id = form.cleaned_data['subrubro'].id
            articulo.cantidad = form.cleaned_data['cantidad']
            articulo.unimed = form.cleaned_data['unimed']  
            articulo.codprovee = form.cleaned_data['codprovee']
            articulo.bajostock = form.cleaned_data['bajostock']
            articulo.deposito = form.cleaned_data['deposito']
            articulo.ubicacion = form.cleaned_data['ubicacion']
            articulo.obs = form.cleaned_data['obs']
            articulo.activo = form.cleaned_data['activo']
            articulo.prodela = form.cleaned_data['prodela']
            articulo.save()
            messages.success(request, 'Artículo guardado.')
            return redirect('lista_articulos')
        else:
            print("❌ Errores:", form.errors)  # <-- Muestra errores
    else:
        form = ArticuloForm(initial={'codart': codigo_sugerido})
    
    contexto = {
        'form': form,
        'codart_auto': codart_auto_activo
    }
    return render(request, 'articulos/formulario.html', contexto)        


def modificar_articulo(request, pk):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')

    articulo = get_object_or_404(Articulo, pk=pk)
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.precosto = round(float(articulo.precosto), 2)
            articulo.margen = round(float(articulo.margen), 2)
            articulo.prefinal = round(float(articulo.prefinal or 0), 2) if articulo.prefinal else None
            articulo.save()
            return redirect('lista_articulos')
    else:
        # Forzar que antes de mostrar el form se recalculen los campos
        articulo.save()  
        form = ArticuloForm(instance=articulo)
    return render(request, 'articulos/formulario.html', {
        'form': form,
        'titulo': 'Editar artículo',
        'es_edicion': True  # <-- nuevo flag
    })

def eliminar_articulo(request, pk):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')

    articulo = get_object_or_404(Articulo, pk=pk)
    articulo.delete()
    return redirect('lista_articulos')
    
def agregar_parametro(request):
    if request.method == 'POST':
        form = ParametroSistemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parámetro guardado correctamente.')
            return redirect('listar_parametros')
        else:
            print("❌ Errores en el formulario:", form.errors)
    else:
        form = ParametroSistemaForm()

    return render(request, 'articulos/agregar_parametro.html', {'form': form})
    
def editar_parametro(request, pk):
    parametro = get_object_or_404(ParametroSistema, pk=pk)
    if request.method == 'POST':
        form = ParametroSistemaForm(request.POST, instance=parametro)
        if form.is_valid():
            form.save()
            return redirect('listar_parametros')
    else:
        form = ParametroSistemaForm(instance=parametro)
    return render(request, 'articulos/editar_parametro.html', {'form': form})
    

def eliminar_parametro(request, pk):
    parametro = get_object_or_404(ParametroSistema, pk=pk)  # 👈 Usás un nombre distinto
    parametro.delete()
    return redirect('listar_parametros')
    
def home_view(request):
    return render(request, 'articulos/home.html')

def listar_parametros(request):
    query = request.GET.get('buscar_parametro', '').strip().upper()

    if query:
        filtros = (
            Q(clave__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(valor__icontains=query)
        )
        parametros = ParametroSistema.objects.filter(filtros)
    else:
        parametros = ParametroSistema.objects.all()

    contexto = {
        'parametros': parametros,
        'query': query
    }

    return render(request, 'articulos/listar_parametros.html', contexto)

from articulos.models import ParametroSistema, Articulo


def obtener_codigo_sugerido():
    ultimo = Articulo.objects.order_by('-codart').first()
    if ultimo and ultimo.codart.isdigit():
        siguiente = str(int(ultimo.codart) + 1).zfill(14)
    else:
        siguiente = "00000000000001"
    return siguiente

