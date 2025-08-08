from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_articulos, name='lista_articulos'),
    # aquí luego puedes agregar modificar_articulo, etc.
]





