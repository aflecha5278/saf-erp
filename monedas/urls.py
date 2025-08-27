from django.urls import path
from . import views
from .views import listado_monedas

urlpatterns = [
    path("", views.listado_monedas, name="listar_monedas"),
    path("alta/", views.alta_moneda, name="alta_moneda"),
    path("editar/<str:pk>/", views.editar_moneda, name="editar_moneda"),
    path('listar/', listado_monedas, name='listado_monedas'),
    path('eliminar/<str:codmoneda>/', views.eliminar_moneda, name='eliminar_moneda') 
]


