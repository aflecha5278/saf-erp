from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Articulo, ParametroSistema
from .forms import ArticuloForm, LoginForm, ParametroSistemaForm 
from django.contrib import messages
from monedas.models import Moneda
import logging
from helpers.parametros import parametro_activo

# Configuración simple de logging (archivo en la raíz del proyecto)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("articulos.log", mode="a", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    logger.addHandler(file_handler)


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

    return render(request, 'login.html', {
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
    return render(request, 'menu.html')    
    

def lista_articulos(request):
    query = request.GET.get('q', '').strip().upper()
    mostrar_moneda = parametro_activo("MONEDA_EXT")

    articulos = Articulo.objects.all().order_by('codart')

    if query:
        articulos = articulos.filter(
            Q(codart__icontains=query) |
            Q(descrip__icontains=query)
        )

    context = {
        "articulos": articulos,
        "mostrar_moneda": mostrar_moneda,
        "query": query
    }

    return render(request, "articulos/lista.html", context )
    

def agregar_articulo(request):
    codart_auto = ParametroSistema.objects.filter(clave='CODART_AUTO').first()
    codart_auto_activo = ParametroSistema.objects.filter(clave='CODART_AUTO', valor='S').exists()
    codigo_sugerido = obtener_codigo_sugerido() if codart_auto_activo else ''
    monedas = Moneda.objects.all()
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, codart_auto_activo=codart_auto_activo)
        if form.is_valid():
            articulo = form.save(commit=False) 
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
            articulo.tipopeso = form.cleaned_data['tipopeso']
            articulo.cotiz = round(float(form.cleaned_data.get('cotiz') or 0), 2)
            articulo.ctome = round(float(form.cleaned_data.get('ctome') or 0), 2)
            articulo.finme = round(float(form.cleaned_data.get('finme') or 0), 2)
            articulo.vtame = round(float(form.cleaned_data.get('vtame') or 0), 2)
            articulo.codmoneda = request.POST.get("codmoneda")
            # Calcular preventa
            articulo.preventa = round(articulo.precosto * (1 + articulo.margen / 100), 2)
            # Asignar alícuota desde la relación
            articulo.alic = articulo.ncodalic.nporc if articulo.ncodalic_id else 0
            articulo.save()
            messages.success(request, 'Artículo guardado.')
            return redirect('lista_articulos')
        else:
            print("❌ Errores:", form.errors)  # <-- Muestra errores
    else:
        form = ArticuloForm(
            initial={
            'codart': codigo_sugerido,
            'codmoneda': 'ARS',
            'cotiz': 1
            },
            codart_auto_activo=codart_auto_activo
        )
    contexto = {
        'form': form,
        'codart_auto': codart_auto_activo,
        'monedas': monedas
    }
    return render(request, 'articulos/formulario.html', contexto)        

def modificar_articulo(request, pk):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')

    articulo = get_object_or_404(Articulo, pk=pk)
    monedas = Moneda.objects.all()
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            articulo.codmoneda = request.POST.get("codmoneda")
            articulo = form.save()  # ← aplica los datos del formulario
            try:
                articulo.precosto = round(float(articulo.precosto or 0), 2)
                articulo.margen = round(float(articulo.margen or 0), 2)
                articulo.prefinal = round(float(articulo.prefinal or 0), 2) if articulo.prefinal else None
            except Exception as e:
                logger.exception("⚠️ Error al convertir campos numéricos: %s", e)

            try:
                articulo.save()
                return redirect('lista_articulos')
            except Exception as e:
                messages.error(request, "Error interno al guardar el artículo.")
        else:
            messages.error(request, f"Errores al guardar: {form.errors.as_text()}")
    else:
        form = ArticuloForm(instance=articulo)

    return render(request, 'articulos/formulario.html', {
        'form': form,
        'titulo': 'Editar artículo',
        'articulo': articulo,
        'monedas': monedas,
        'es_edicion': True
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
    return render(request, 'home.html')

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

def obtener_codigo_sugerido():
    ultimo = Articulo.objects.order_by('-codart').first()
    if ultimo and ultimo.codart.isdigit():
        siguiente = str(int(ultimo.codart) + 1).zfill(14)
    else:
        siguiente = "00000000000001"
    return siguiente
    

def page2_moneda_ext(request, codart):
    articulo = get_object_or_404(Articulo, codart=codart)
    form = ArticuloForm(request.POST or None, instance=articulo)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('listado_articulos')

    monedas = Moneda.objects.all()

    return render(request, 'articulos/form_moneda_ext.html', {
        'form': form,
        'articulo': articulo,
        'monedas': monedas,
        'alicuota': articulo.ncodalic.nporc if articulo.ncodalic_id else 0,
    })


