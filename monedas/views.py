from django.shortcuts import render, redirect, get_object_or_404
from .models import Moneda
from .forms import MonedaForm
from django.contrib import messages

def home_view(request):
    return render(request, "home.html")

def login_view(request):
    return render(request, "login.html")
    
def menu_principal(request):
    return render(request, "menu.html")
    
# 🧾 Listado de monedas
def listado_monedas(request):
    monedas = Moneda.objects.all().order_by("codmoneda")
    return render(request, "monedas/listado.html", {
        "monedas": monedas,
        "titulo": "Listado de Monedas",
    })

# ➕ Alta de moneda
def alta_moneda(request):
    form = MonedaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("listado_monedas")
    return render(request, "monedas/formulario.html", {
        "form": form,
        "modo": "alta",
        "titulo": "Alta de Moneda",
    })

def editar_moneda(request, pk):
    moneda = get_object_or_404(Moneda, codmoneda=pk)
    form = MonedaForm(request.POST or None, instance=moneda)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('listado_monedas')
    return render(request, 'monedas/formulario.html', {'form': form})
    
 
def eliminar_moneda(request, codmoneda):
    moneda = get_object_or_404(Moneda, codmoneda=codmoneda)
    moneda.delete()
    messages.success(request, f"La moneda '{moneda.descrip}' fue eliminada correctamente.")
    return redirect('listado_monedas')
 
    

